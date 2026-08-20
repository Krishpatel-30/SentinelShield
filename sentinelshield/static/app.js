/* SentinelShield desk — keep this file as the only page script */
let TOKEN = localStorage.getItem("ss_token") || "";
let USER = null;
let DATA = { alerts: [], watchlist: [], chat: [], cities: [] };
let CAMS = [];
let CITY = "", AREA = "", AREAS = [];
let map, markers = [];
let ws;
let chatOpen = false;

const $ = (id) => document.getElementById(id);
const fmt = (n) => (n || 0).toLocaleString("en-IN");

async function doLogin() {
  const fd = new FormData();
  fd.append("username", $("user").value);
  fd.append("password", $("pass").value);
  const r = await fetch("/api/login", { method: "POST", body: fd });
  const j = await r.json();
  if (!j.ok) { alert(j.error || "Login failed"); return; }
  TOKEN = j.token; USER = j.user;
  localStorage.setItem("ss_token", TOKEN);
  showApp();
}
function logout() {
  TOKEN = ""; USER = null; localStorage.removeItem("ss_token");
  $("app").classList.add("hidden"); $("login").classList.remove("hidden");
}
function showApp() {
  $("login").classList.add("hidden"); $("app").classList.remove("hidden");
  $("who").textContent = USER ? (USER.name + " · " + USER.role) : "";
  refresh();
  openWs();
  setInterval(refresh, 5000);
}
function tab(name, btn) {
  document.querySelectorAll("nav button").forEach((b) => b.classList.remove("on"));
  if (btn) btn.classList.add("on");
  document.querySelectorAll(".page > section").forEach((el) => {
    el.classList.toggle("hidden", el.id !== "p-" + name);
  });
  if (name === "map" || name === "twin") setTimeout(drawTwin, 50);
  if (name === "find") setTimeout(() => { if (window._lastFind) drawFindMap(window._lastFind); }, 50);
  if (name === "cams" && CITY && AREA) loadCams();
  if (name === "home" && CITY && AREA) loadCams();
  if (name === "live") renderLive();
  if (name === "tools") fillTools();
  if (name === "webcam" && window.WebcamTest) window.WebcamTest.onShow();
}
function toggleChat() {
  chatOpen = !chatOpen;
  $("chatdraw").classList.toggle("hidden", !chatOpen);
  $("chatback").classList.toggle("hidden", !chatOpen);
  if (chatOpen) $("chatlog").scrollTop = $("chatlog").scrollHeight;
}
function badge(cam) {
  if (cam.status === "tampered") return '<span class="badge b-bad">TAMPER</span>';
  if (cam.status === "checking") return '<span class="badge b-warn">CHECKING</span>';
  if (cam.status === "live") return '<span class="badge b-info">LIVE</span>';
  if (cam.status === "checked") return '<span class="badge b-good">OK ' + cam.trust + "</span>";
  if (cam.live_url) return '<span class="badge b-info">LINK SAVED</span>';
  if (cam.kind === "registry") return '<span class="badge b-info">GOVT</span>';
  return '<span class="badge b-info">' + (cam.status || "ready") + "</span>";
}
function camCard(c) {
  const hasVid = c.source && c.kind === "recorded";
  return `<article class="cam">
    <h3>${c.name} ${badge(c)}</h3>
    <div class="meta">${c.owner || "Government"}<br/>${c.spot || c.place || ""}<br/>${c.last_note || ""}</div>
    <div class="row">
      ${hasVid
        ? `<button class="btn btn-g" onclick="analyze('${c.id}')">Check video + threats</button>`
        : `<span class="meta">Upload a clip or add a live link in Live tab.</span>`}
      <label class="btn btn-s">Upload<input type="file" accept="video/*" hidden onchange="upload('${c.id}', this)"/></label>
    </div>
  </article>`;
}
function renderHome() {
  if ($("estate-n")) $("estate-n").textContent = fmt(DATA.estate_total) + "+";
  const threats = (DATA.alerts || []).filter((a) => a.kind === "threat" || a.kind === "watchlist" || a.kind === "tamper");
  if ($("stats")) {
    $("stats").innerHTML = `
      <div class="stat"><b>${fmt(DATA.estate_total)}</b> Gujarat gov cameras</div>
      <div class="stat"><b>${(DATA.cities || []).length}</b> cities / groups</div>
      <div class="stat"><b>${threats.filter((a) => a.status === "new").length}</b> open threats</div>`;
  }
  let crumb = `<button onclick="backLevel(0)">Gujarat</button>`;
  if (CITY) {
    const c = (DATA.cities || []).find((x) => x.id === CITY);
    crumb += ` → <button onclick="backLevel(1)">${c ? c.name : CITY}</button>`;
  }
  if (AREA) {
    const a = AREAS.find((x) => x.id.endsWith(":" + AREA) || x.id === AREA);
    crumb += ` → <span>${a ? a.name : AREA}</span>`;
  }
  if ($("crumb")) $("crumb").innerHTML = crumb;

  if (!CITY) {
    $("home-grid").innerHTML = (DATA.cities || []).map((c) => `
      <article class="cam citypick" onclick="pickCity('${c.id}')">
        <h3>${c.name}</h3>
        <div class="meta">Government cameras in this city</div>
        <b style="font-size:22px;color:var(--accent)">${fmt(c.cameras)}</b>
      </article>`).join("");
    return;
  }
  if (!AREA) {
    $("home-grid").innerHTML = AREAS.map((a) => {
      const aid = a.id.includes(":") ? a.id.split(":")[1] : a.id;
      return `<article class="cam citypick" onclick="pickArea('${aid}')">
        <h3>${a.name}</h3>
        <div class="meta">Select this area</div>
        <b style="font-size:22px;color:var(--accent)">${fmt(a.cameras)}</b>
      </article>`;
    }).join("");
    return;
  }
  $("home-grid").innerHTML = CAMS.map(camCard).join("") || "<p class='meta'>No cameras in this area yet.</p>";
}
function render() {
  renderHome();
  if ($("cam-list")) $("cam-list").innerHTML = CAMS.map(camCard).join("");
  const allA = DATA.alerts || [];
  const threats = allA.filter((a) => a.kind === "threat" || a.kind === "watchlist");
  if ($("threat-rows")) $("threat-rows").innerHTML = threats.map(alertRow).join("") || "<tr><td colspan='5'>No threats yet.</td></tr>";
  if ($("alert-rows")) $("alert-rows").innerHTML = allA.map(alertRow).join("") || "<tr><td colspan='5'>No alerts.</td></tr>";
  if ($("wl-rows")) {
    $("wl-rows").innerHTML = (DATA.watchlist || []).map((w) => `<tr>
      <td><b>${w.plate}</b></td><td>${w.kind}</td><td>${w.note || ""}</td>
      <td><button class="btn btn-r" onclick="delWl('${w.id}')">Remove</button></td></tr>`).join("");
  }
  if ($("person-rows")) {
    $("person-rows").innerHTML = (DATA.persons || []).map((p) =>
      `<tr><td>${p.name}</td><td>${p.kind}</td><td>${p.note || ""}</td></tr>`).join("");
  }
  if ($("ev-cam")) {
    $("ev-cam").innerHTML = (DATA.demoCams || CAMS.filter((c) => c.kind === "recorded")).map((c) =>
      `<option value="${c.id}">${c.name}</option>`).join("");
  }
  renderLive();
  if ($("ai-status") && DATA.ai) {
    $("ai-status").textContent = DATA.ai.on
      ? ("AI ON · last " + (DATA.ai.last_cam || "—") + " · cycle " + (DATA.ai.cycles || 0))
      : "AI paused";
  }
  if ($("chatdot")) $("chatdot").textContent = (DATA.chat || []).length;
  const log = $("chatlog");
  if (log) {
    const stick = log.scrollTop + log.clientHeight >= log.scrollHeight - 50;
    log.innerHTML = (DATA.chat || []).map((m) => `<div class="msg"><b>${m.user}</b>
      <span class="t">${(m.created || "").slice(11, 19)}</span><p>${escapeHtml(m.text)}</p></div>`).join("");
    if (stick || chatOpen) log.scrollTop = log.scrollHeight;
  }
}
function alertRow(a) {
  return `<tr>
    <td>${a.created}</td>
    <td><b>${a.title}</b><br/><span class="meta">${a.detail || ""} · ${a.kind}</span></td>
    <td>${a.camera_id}</td>
    <td>${a.trust}</td>
    <td>
      <span class="badge ${a.severity === "CRITICAL" ? "b-bad" : "b-warn"}">${a.severity}</span>
      <div class="row">
        <button class="btn btn-d" onclick="setAlert('${a.id}','seen')">Seen</button>
        <button class="btn btn-g" onclick="setAlert('${a.id}','done')">Done</button>
      </div>
      <div class="meta">${a.status}</div>
    </td></tr>`;
}
function escapeHtml(s) {
  return String(s || "").replace(/[&<>"]/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]));
}
async function refresh() {
  const r = await fetch("/api/overview");
  DATA = await r.json();
  if (CITY && AREA) await loadCams(false);
  else if (CITY) await loadAreas();
  render();
}
async function pickCity(id) {
  CITY = id; AREA = ""; CAMS = [];
  await loadAreas();
  render();
}
async function pickArea(id, stay) {
  AREA = id;
  await loadCams();
  render();
  if (stay === "live") tab("live", document.querySelector('[data-tab="live"]'));
  else tab("cams", document.querySelector('[data-tab="cams"]'));
}
function backLevel(n) {
  if (n === 0) { CITY = ""; AREA = ""; AREAS = []; CAMS = []; }
  if (n === 1) { AREA = ""; CAMS = []; }
  render();
  tab("home", document.querySelector('[data-tab="home"]'));
}
async function loadAreas() {
  const r = await fetch("/api/areas?city=" + encodeURIComponent(CITY));
  const j = await r.json();
  AREAS = j.areas || [];
}
async function loadCams(doRender) {
  const r = await fetch("/api/cameras?owner=government&city=" + encodeURIComponent(CITY) + "&area=" + encodeURIComponent(AREA));
  const j = await r.json();
  CAMS = j.cameras || [];
  if (doRender) render();
}
async function analyze(id) {
  await fetch("/api/analyze/" + id, { method: "POST" });
  refresh();
}
async function analyzeAll() {
  for (const c of CAMS.filter((x) => x.kind === "recorded")) await analyze(c.id);
}
async function upload(id, input) {
  if (!input.files[0]) return;
  const fd = new FormData();
  fd.append("camera_id", id);
  fd.append("file", input.files[0]);
  await fetch("/api/upload", { method: "POST", body: fd });
  input.value = "";
  loadCams();
}
async function addCam() {
  if (!CITY || !AREA) { alert("First open a city and an area."); return; }
  const fd = new FormData();
  fd.append("name", $("nc-name").value || "New camera");
  fd.append("city_id", CITY);
  fd.append("area_id", AREA);
  fd.append("owner", "Gujarat Police");
  fd.append("place", (DATA.cities || []).find((c) => c.id === CITY)?.name || "Gujarat");
  await fetch("/api/cameras", { method: "POST", body: fd });
  $("nc-name").value = "";
  loadCams();
}
async function addWl() {
  const fd = new FormData();
  fd.append("plate", $("wl-plate").value);
  fd.append("kind", $("wl-kind").value);
  fd.append("note", $("wl-note").value);
  await fetch("/api/watchlist", { method: "POST", body: fd });
  $("wl-plate").value = ""; $("wl-note").value = "";
  refresh();
}
async function delWl(id) { await fetch("/api/watchlist/" + id, { method: "DELETE" }); refresh(); }
async function setAlert(id, status) {
  const fd = new FormData(); fd.append("status", status);
  await fetch("/api/alerts/" + id + "/status", { method: "POST", body: fd });
  refresh();
}

function renderLive() {
  const crumb = $("live-crumb");
  const grid = $("live-grid");
  const bind = $("live-bind");
  if (!crumb || !grid) return;
  let html = `<button type="button" onclick="liveBack(0)">Gujarat</button>`;
  if (CITY) {
    const c = (DATA.cities || []).find((x) => x.id === CITY);
    html += ` → <button type="button" onclick="liveBack(1)">${c ? c.name : CITY}</button>`;
  }
  if (AREA) {
    const a = AREAS.find((x) => x.id.endsWith(":" + AREA) || x.id === AREA);
    html += ` → <span>${a ? a.name : AREA}</span>`;
  }
  crumb.innerHTML = html;
  if (!CITY) {
    grid.innerHTML = (DATA.cities || []).map((c) => `
      <article class="cam citypick" onclick="livePickCity('${c.id}')">
        <h3>${c.name}</h3>
        <div class="meta">Open this city</div>
        <b style="font-size:22px;color:var(--accent)">${fmt(c.cameras)}</b>
      </article>`).join("");
  } else if (!AREA) {
    grid.innerHTML = AREAS.map((a) => {
      const aid = a.id.includes(":") ? a.id.split(":")[1] : a.id;
      return `<article class="cam citypick" onclick="livePickArea('${aid}')">
        <h3>${a.name}</h3>
        <div class="meta">Government cameras in this area</div>
        <b style="font-size:22px;color:var(--accent)">${fmt(a.cameras)}</b>
      </article>`;
    }).join("");
  } else {
    grid.innerHTML = CAMS.map(liveCard).join("") || "<p class='meta'>No cameras listed in this area.</p>";
  }
  if (bind) bind.innerHTML = CAMS.map((c) => `<option value="${c.id}">${c.name}</option>`).join("");
}
function liveCard(c) {
  const hasLink = !!c.live_url;
  const hasFile = !!(c.source && (c.kind === "recorded" || c.kind === "live"));
  return `<article class="cam">
    <h3>${c.name} ${badge(c)}</h3>
    <div class="meta">${c.owner || ""} · ${c.spot || ""}<br/>
      ${hasLink ? "Live link saved" : (hasFile ? "Demo clip ready" : "Add a live link")}</div>
    <div class="row">
      <button class="btn btn-g" onclick="startLive('${c.id}')">Open live</button>
    </div>
  </article>`;
}
async function livePickCity(id) {
  CITY = id; AREA = ""; CAMS = [];
  await loadAreas();
  renderLive();
}
async function livePickArea(id) {
  AREA = id;
  await loadCams(false);
  renderLive();
}
function liveBack(n) {
  if (n === 0) { CITY = ""; AREA = ""; AREAS = []; CAMS = []; }
  if (n === 1) { AREA = ""; CAMS = []; }
  renderLive();
}
async function startLive(id) {
  const camId = id || ($("live-bind") && $("live-bind").value);
  if (!camId) { alert("First pick city then area, then a camera."); return; }
  const fd = new FormData();
  fd.append("camera_id", camId);
  fd.append("source", "auto");
  const r = await fetch("/api/live/start", { method: "POST", body: fd });
  const j = await r.json();
  if (!r.ok) { alert(j.error || "Cannot start live"); return; }
  if ($("live-now")) $("live-now").textContent = "Playing " + camId;
  $("live-img").src = "/api/live/stream?t=" + Date.now();
}
async function saveLiveLink() {
  const id = $("live-bind") && $("live-bind").value;
  const url = ($("live-url") && $("live-url").value.trim()) || "";
  if (!id) { alert("Open city and area first so the camera list fills."); return; }
  if (!url) { alert("Paste rtsp:// or http:// link from your shop camera."); return; }
  const fd = new FormData();
  fd.append("live_url", url);
  const r = await fetch("/api/cameras/" + id + "/connect", { method: "POST", body: fd });
  const j = await r.json();
  if (!r.ok) { alert(j.error || "Could not save"); return; }
  $("live-url").value = "";
  await loadCams(false);
  renderLive();
  alert("Link saved. Press Open live.");
}
async function addShopCam() {
  const name = ($("shop-name") && $("shop-name").value.trim()) || "My shop camera";
  const url = ($("shop-url") && $("shop-url").value.trim()) || "";
  if (!url) { alert("Paste your shop camera link (rtsp:// or http://)."); return; }
  if (!CITY || !AREA) { alert("On Live tab: pick your city, then area, then add the shop camera."); return; }
  const fd = new FormData();
  fd.append("name", name);
  fd.append("live_url", url);
  fd.append("city_id", CITY);
  fd.append("area_id", AREA);
  fd.append("owner", "Shop / private");
  fd.append("place", (DATA.cities || []).find((c) => c.id === CITY)?.name || "Gujarat");
  const r = await fetch("/api/cameras", { method: "POST", body: fd });
  const j = await r.json();
  if (!r.ok) { alert("Could not add camera"); return; }
  $("shop-name").value = "";
  $("shop-url").value = "";
  await loadCams(false);
  renderLive();
  alert("Shop camera added. Press Open live on its card.");
}
async function stopLive() {
  await fetch("/api/live/stop", { method: "POST" });
  if ($("live-img")) $("live-img").removeAttribute("src");
  if ($("live-now")) $("live-now").textContent = "Live stopped.";
}
function openWs() {
  const proto = location.protocol === "https:" ? "wss" : "ws";
  ws = new WebSocket(proto + "://" + location.host + "/ws");
  ws.onmessage = (ev) => {
    const m = JSON.parse(ev.data);
    if (m.type === "chat") {
      DATA.chat = DATA.chat || [];
      DATA.chat.push(m);
      render();
    }
  };
}
async function sendChat(e) {
  e.preventDefault();
  const text = $("chatbox").value.trim();
  if (!text) return;
  if (ws && ws.readyState === 1) {
    ws.send(JSON.stringify({ type: "chat", token: TOKEN, text: text, room: "team" }));
  } else {
    const fd = new FormData();
    fd.append("text", text); fd.append("token", TOKEN);
    await fetch("/api/chat", { method: "POST", body: fd });
    refresh();
  }
  $("chatbox").value = "";
}
function drawMap() {
  if (!window.L) return;
  const c = (DATA.cities || []).find((x) => x.id === CITY);
  const center = c ? [c.lat, c.lng] : [22.3, 71.2];
  if (!map) {
    map = L.map("map").setView(center, CITY ? 11 : 7);
    L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", { maxZoom: 18 }).addTo(map);
  } else map.setView(center, CITY ? 12 : 7);
  markers.forEach((m) => map.removeLayer(m));
  markers = [];
  CAMS.forEach((cam) => {
    if (cam.lat == null) return;
    const color = cam.status === "tampered" ? "red" : (cam.status === "checked" ? "green" : "#38bdf8");
    const m = L.circleMarker([cam.lat, cam.lng], { radius: 8, color: color }).addTo(map);
    m.bindPopup("<b>" + cam.name + "</b><br/>" + (cam.owner || ""));
    markers.push(m);
  });
  setTimeout(() => map.invalidateSize(), 200);
}
async function searchPlate() {
  try {
    const a = $("qplate") ? $("qplate").value : "";
    const b = $("qplate2") ? $("qplate2").value : "";
    const p = (a || b || "").trim();
    if (!p) { alert("Type a vehicle number, e.g. GJ05SS2026"); return; }
    if ($("qplate")) $("qplate").value = p;
    if ($("qplate2")) $("qplate2").value = p;
    tab("find", document.querySelector('[data-tab="find"]'));
    const r = await fetch("/api/vehicle?plate=" + encodeURIComponent(p));
    const j = await r.json();
    window._lastFind = j;
    if ($("find-msg")) $("find-msg").textContent = j.message || j.error || "";
    if (j.last && $("find-last")) {
      $("find-last").innerHTML = '<div class="box" style="margin-top:10px"><h3>Last seen: ' +
        escapeHtml(j.plate) + "</h3><p><b>" + escapeHtml(j.last.camera_name || "") +
        "</b> · " + escapeHtml(j.last.place || "") + " · " + escapeHtml(j.last.created || "") +
        "</p>" + (j.watchlist ? '<span class="badge b-bad">' + escapeHtml(j.watchlist.kind) +
        " — " + escapeHtml(j.watchlist.note || "") + "</span>" : "") + "</div>";
    } else if ($("find-last")) {
      $("find-last").innerHTML = "";
    }
    if ($("find-rows")) {
      $("find-rows").innerHTML = (j.history || []).map(function (h) {
        return "<tr><td>" + escapeHtml(h.created) + "</td><td>" + escapeHtml(h.camera_name) +
          "</td><td>" + escapeHtml(h.place || "") + "</td><td>" + escapeHtml(h.city_id || "") + "</td></tr>";
      }).join("") || "<tr><td colspan='4'>No history yet.</td></tr>";
    }
    setTimeout(function () { drawFindMap(j); }, 100);
  } catch (err) {
    alert("Find failed: " + err);
  }
}
let findMap = null;
let findMarks = [];
function drawFindMap(j) {
  if (!window.L || !$("find-map")) return;
  const last = j && j.last;
  const center = last && last.lat ? [last.lat, last.lng] : [21.17, 72.83];
  if (!findMap) {
    findMap = L.map("find-map").setView(center, 12);
    L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", { maxZoom: 18 }).addTo(findMap);
  } else {
    findMap.setView(center, 13);
  }
  findMarks.forEach(function (m) { findMap.removeLayer(m); });
  findMarks = [];
  (j.history || []).forEach(function (h, i) {
    if (h.lat == null) return;
    const m = L.circleMarker([h.lat, h.lng], { radius: i === 0 ? 11 : 7, color: i === 0 ? "#e11d48" : "#38bdf8" }).addTo(findMap);
    m.bindPopup((i === 0 ? "LAST · " : "") + h.camera_name + "<br/>" + h.created);
    findMarks.push(m);
  });
  setTimeout(function () { findMap.invalidateSize(); }, 250);
}
async function toggleAi() {
  const on = DATA.ai && DATA.ai.on;
  await fetch(on ? "/api/ai/off" : "/api/ai/on", { method: "POST" });
  refresh();
}
async function loadEvents() {
  const r = await fetch("/api/events");
  const j = await r.json();
  const rows = (j.events || []).slice(0, 20);
  const html = rows.map((e) => {
    let what = e.title || e.kind;
    if (e.kind === "vehicle") what = "Vehicle number seen: " + (e.extra || e.title);
    if (e.kind === "tamper") what = "Camera picture frozen / black";
    if (e.kind === "crowd" || e.kind === "panic") what = "Crowd / people running";
    return "<tr><td>" + escapeHtml(e.created || "") + "</td><td><b>" + escapeHtml(what) +
      "</b></td><td>" + escapeHtml(e.place || e.camera_id || "") + "</td></tr>";
  }).join("") || "<tr><td colspan='3'>Waiting for AI… keep this page open 15 seconds.</td></tr>";
  if ($("tools-ev-rows")) $("tools-ev-rows").innerHTML = html;
  if ($("ev-rows")) $("ev-rows").innerHTML = html;
  if ($("tools-stats")) {
    $("tools-stats").innerHTML =
      '<div class="stat"><b>' + rows.length + "</b> latest finds</div>" +
      '<div class="stat"><b>' + ((DATA.ai && DATA.ai.cycles) || 0) + "</b> AI checks done</div>" +
      '<div class="stat"><b>' + ((DATA.alerts || []).filter((a) => a.status === "new").length) + "</b> new alerts</div>";
  }
}
async function loadCyber() {
  const r = await fetch("/api/cyber");
  const j = await r.json();
  const html = (j.cyber || []).map((e) =>
    "<tr><td>" + escapeHtml(e.created || "") + "</td><td>" + escapeHtml(e.kind) +
    "</td><td>" + escapeHtml(e.detail || "") + "</td></tr>"
  ).join("") || "<tr><td colspan='3'>No cyber hits yet. Press the red button to test.</td></tr>";
  if ($("tools-cyber-rows")) $("tools-cyber-rows").innerHTML = html;
}
async function loadVault() {
  let packs = [];
  let ranked = [];
  try { packs = (await (await fetch("/api/evidence")).json()).packs || []; } catch (e) {}
  try { ranked = (await (await fetch("/api/rank-evidence")).json()).ranked || []; } catch (e) {}
  let html = ranked.slice(0, 8).map((e) =>
    "<tr><td>" + escapeHtml(e.created || "") + "</td><td>Score " + (e.rank_score || "") +
    " · " + escapeHtml(e.kind || "") + "</td><td>" + escapeHtml(e.title || "") + "</td></tr>"
  ).join("");
  html += packs.map((e) =>
    "<tr><td>" + escapeHtml(e.created || "") + "</td><td>Saved file</td><td style='font-size:11px'>" +
    escapeHtml((e.sha256 || "").slice(0, 24)) + "…</td></tr>"
  ).join("");
  if ($("tools-evd-rows")) $("tools-evd-rows").innerHTML = html || "<tr><td colspan='3'>Press Save evidence now.</td></tr>";
  try {
    const hc = await (await fetch("/api/hot-cams")).json();
    if ($("ev-cam")) {
      $("ev-cam").innerHTML = (hc.cameras || []).map((c) =>
        '<option value="' + c.id + '">' + c.name + "</option>").join("");
    }
  } catch (e) {}
}
async function fillTools() {
  await loadEvents();
  await loadCyber();
  await loadVault();
}
async function sealEvidence() {
  const id = ($("ev-cam") && $("ev-cam").value) || "cam-gate";
  const r = await fetch("/api/evidence/" + id, { method: "POST" });
  const j = await r.json();
  if (!r.ok) { alert(j.error || "Could not save"); return; }
  alert("Saved. Fingerprint:\n" + (j.sha256 || "").slice(0, 32) + "…");
  loadVault();
}
document.addEventListener("click", function (e) {
  const t = e.target;
  const id = t && t.id;
  if (t && t.getAttribute && t.getAttribute("data-ask")) {
    if ($("askq")) $("askq").value = t.getAttribute("data-ask");
    askBot();
    return;
  }
  if (id === "btn-find" || id === "btn-find2") searchPlate();
  if (id === "btn-ai") toggleAi();
  if (id === "btn-evq") loadEvents();
  if (id === "btn-evd") sealEvidence();
  if (id === "btn-heat") { tab("map", document.querySelector('[data-tab="map"]')); setTimeout(() => drawTwin("heat"), 80); }
  if (id === "btn-cybermap") { tab("map", document.querySelector('[data-tab="map"]')); setTimeout(() => drawTwin("cyber"), 80); }
  if (id === "btn-route") { if ($("qplate")) $("qplate").value = "GJ05SS2026"; searchPlate(); }
  if (id === "btn-drone") launchDrone();
  if (id === "btn-panic") fetch("/api/demo/panic", { method: "POST" }).then(() => { refresh(); tab("alerts", document.querySelector('[data-tab="alerts"]')); });
  if (id === "btn-bag") fetch("/api/demo/abandoned", { method: "POST" }).then(() => { refresh(); tab("alerts", document.querySelector('[data-tab="alerts"]')); });
  if (id === "btn-hp") fetch("/honeypot").then(() => { fillTools(); refresh(); });
  if (id === "btn-ask") askBot();
  if (id === "btn-voice") startVoice();
});
document.addEventListener("keydown", function (e) {
  if (e.key === "Enter" && (e.target.id === "qplate" || e.target.id === "qplate2")) {
    e.preventDefault();
    searchPlate();
  }
});
let twinMap = null, twinLayer = [];
async function drawTwin(mode) {
  if (!window.L || !$("twin-map")) return;
  const heat = await (await fetch("/api/heat")).json();
  const twin = await (await fetch("/api/twin")).json();
  if (!twinMap) {
    twinMap = L.map("twin-map").setView([22.5, 71.8], 7);
    L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", { maxZoom: 18 }).addTo(twinMap);
  }
  twinLayer.forEach((m) => twinMap.removeLayer(m));
  twinLayer = [];
  const showHeat = !mode || mode === "heat" || mode === "route";
  const showCyber = !mode || mode === "cyber";
  if (showHeat) {
    (heat.spots || []).forEach((s) => {
      const r = s.level === "high" ? 28 : (s.level === "medium" ? 18 : 10);
      const col = s.level === "high" ? "#e11d48" : (s.level === "medium" ? "#f59e0b" : "#22c55e");
      const m = L.circleMarker([s.lat, s.lng], { radius: r, color: col, fillOpacity: 0.35 }).addTo(twinMap);
      m.bindPopup("<b>" + s.name + "</b><br/>Past incidents: " + s.past + "<br/>Predicted risk: " + s.predicted + " (" + s.level + ")");
      twinLayer.push(m);
    });
  }
  (twin.cameras || []).forEach((c) => {
    if (c.lat == null) return;
    const m = L.circleMarker([c.lat, c.lng], { radius: 6, color: "#38bdf8" }).addTo(twinMap);
    m.bindPopup(c.name + "<br/>" + (c.place || ""));
    twinLayer.push(m);
  });
  if (showCyber) {
    (twin.cyber || []).forEach((cy) => {
      const cam = (twin.cameras || []).find((c) => c.id === cy.camera_id) || { lat: 23.02, lng: 72.57 };
      if (cam.lat == null) return;
      const m = L.circleMarker([cam.lat, cam.lng], { radius: 10, color: "#fb923c" }).addTo(twinMap);
      m.bindPopup("CYBER · " + cy.kind + "<br/>" + cy.detail);
      twinLayer.push(m);
    });
  }
  if (mode === "route") {
    const rt = await (await fetch("/api/route?plate=GJ05SS2026")).json();
    const latlngs = (rt.points || []).filter((p) => p.lat != null).map((p) => [p.lat, p.lng]);
    if (latlngs.length) {
      const line = L.polyline(latlngs, { color: "#e11d48" }).addTo(twinMap);
      twinLayer.push(line);
      twinMap.fitBounds(line.getBounds(), { padding: [30, 30] });
      if ($("twin-note")) $("twin-note").textContent = "Route hops " + rt.hops + " · direction " + rt.direction + " · est " + (rt.speed_kmh_est || "—") + " km/h";
    }
  } else if ($("twin-note")) {
    $("twin-note").textContent = "Red = predicted high risk · Orange = cyber · Blue = cameras. Heat is history + density, not a crystal ball.";
  }
  setTimeout(() => twinMap.invalidateSize(), 200);
}
async function launchDrone() {
  const fd = new FormData();
  fd.append("city", CITY || "surat");
  fd.append("reason", "CCTV alert");
  const j = await (await fetch("/api/drones/launch", { method: "POST", body: fd })).json();
  alert(j.drone + " " + j.status + "\n" + j.feed);
  tab("map", document.querySelector('[data-tab="map"]'));
}
async function askBot() {
  const q = ($("askq") && $("askq").value) || "";
  if (!q) return;
  const fd = new FormData();
  fd.append("q", q);
  const j = await (await fetch("/api/ask", { method: "POST", body: fd })).json();
  let msg = j.note || j.hint || ("Done: " + (j.intent || "ok"));
  if (j.intent === "watchlist" && j.data) {
    msg = "Blacklisted / stolen numbers:\n" + j.data.map((w) => w.plate + " — " + (w.note || w.kind)).join("\n");
  }
  if (j.intent === "alerts" && j.data) {
    msg = "Latest alerts:\n" + j.data.slice(0, 6).map((a) => a.title).join("\n");
  }
  if (j.intent === "cyber" && j.data) {
    msg = "Cyber hits:\n" + j.data.slice(0, 6).map((a) => a.kind + " — " + a.detail).join("\n");
  }
  if ($("ask-out")) $("ask-out").textContent = msg;
  if (j.tab && j.tab !== "help" && document.querySelector('[data-tab="' + j.tab + '"]')) {
    tab(j.tab, document.querySelector('[data-tab="' + j.tab + '"]'));
  }
  if (j.intent === "vehicle") { if ($("qplate")) $("qplate").value = "GJ05SS2026"; searchPlate(); }
}
function startVoice() {
  const Rec = window.SpeechRecognition || window.webkitSpeechRecognition;
  if (!Rec) { alert("This browser has no voice input. Type in Ask instead."); return; }
  const r = new Rec();
  r.lang = "en-IN";
  r.onresult = function (ev) {
    const said = ev.results[0][0].transcript;
    if ($("askq")) $("askq").value = said;
    askBot();
  };
  r.start();
}
function boot() {
  try {
    if ($("login")) $("login").classList.remove("hidden");
    if ($("app")) $("app").classList.add("hidden");
  } catch (e) {}
  if (!TOKEN) return;
  fetch("/api/me?token=" + encodeURIComponent(TOKEN))
    .then((r) => r.json())
    .then((j) => {
      if (j.ok) { USER = j.user; showApp(); }
    })
    .catch(function () {});
}
if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", boot);
else boot();
