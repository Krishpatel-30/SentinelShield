/* =====================================================================
   TEMP WEBCAM / IP WEBCAM TEST — delete this file to remove the feature.
   Search TEMP WEBCAM / TEMP_WEBCAM in index.html and app.js too.
   ===================================================================== */
(function () {
  let stream = null;
  let shotTimer = null;

  function $(id) { return document.getElementById(id); }

  function log(msg) {
    const el = $("wc-log");
    if (!el) return;
    el.textContent = "[" + new Date().toLocaleTimeString() + "] " + msg + "\n" + el.textContent;
  }

  function normalizeLink(raw) {
    let u = (raw || "").trim();
    u = u.replace(/\/+$/, "");
    u = u.replace(/\/(video|videofeed|shot\.jpg).*$/i, "");
    if (u && !/^https?:\/\//i.test(u)) u = "http://" + u;
    return u;
  }

  function savedList() {
    try { return JSON.parse(localStorage.getItem("ss_ipwebcam_list") || "[]"); } catch (e) { return []; }
  }

  function writeList(arr) {
    localStorage.setItem("ss_ipwebcam_list", JSON.stringify(arr));
    localStorage.setItem("ss_ipwebcam", arr[0] || "");
  }

  function showSaved() {
    const el = $("wc-saved");
    if (!el) return;
    const arr = savedList();
    if (!arr.length) { el.textContent = "No link saved yet. Paste the IP Webcam address and press Add this link."; return; }
    el.innerHTML = "Saved links: " + arr.map(function (u, i) {
      return '<button type="button" class="btn btn-s wc-use" data-url="' + u.replace(/"/g, "") + '">' + u + "</button>";
    }).join(" ");
    if ($("wc-url") && !$("wc-url").value) $("wc-url").value = arr[0];
  }

  function addLink() {
    const u = normalizeLink($("wc-url") && $("wc-url").value);
    if (!u || u === "http://") {
      alert("Paste the link from IP Webcam, e.g. http://192.168.1.25:8080");
      return;
    }
    const arr = savedList().filter(function (x) { return x !== u; });
    arr.unshift(u);
    writeList(arr.slice(0, 6));
    $("wc-url").value = u;
    showSaved();
    log("Link added: " + u);
    $("wc-readout").textContent = "Link saved. Now press Show live video.";
  }

  function baseUrl() {
    return normalizeLink($("wc-url") && $("wc-url").value);
  }

  function setOn(on, text) {
    const s = $("wc-status");
    if (!s) return;
    s.textContent = on ? (text || "LIVE") : "OFF";
    s.className = "badge " + (on ? "b-good" : "b-info");
  }

  function stopAll() {
    if (shotTimer) { clearInterval(shotTimer); shotTimer = null; }
    if (stream) {
      stream.getTracks().forEach(function (t) { t.stop(); });
      stream = null;
    }
    const v = $("wc-video");
    if (v) { v.srcObject = null; v.classList.add("hidden"); }
    const img = $("wc-ipimg");
    if (img) { img.removeAttribute("src"); img.style.display = "none"; }
    setOn(false);
    log("Stopped.");
  }

  function showRelay() {
    stopAll();
    const img = $("wc-ipimg");
    if (!img) return;
    img.style.display = "block";
    function tick() {
      img.src = "/api/temp/webcam-relay.jpg?t=" + Date.now();
    }
    img.onerror = function () {
      $("wc-readout").textContent = "Waiting for phone… Open /phone-send on the phone and tap Start sending.";
    };
    img.onload = function () {
      setOn(true, "PHONE (ANY WIFI)");
      $("wc-readout").textContent = "Phone picture arriving. Not same Wi‑Fi.";
    };
    tick();
    shotTimer = setInterval(tick, 400);
    log("Watching relay. Open /phone-send on the phone.");
  }

  function showPhoneVideo() {
    const b = baseUrl();
    if (!b) { alert("Type the address shown in IP Webcam (example http://192.168.1.25:8080)"); return; }
    stopAll();
    const img = $("wc-ipimg");
    img.style.display = "block";
    // IP Webcam live MJPEG
    img.src = b + "/video";
    img.onerror = function () {
      log("Live /video failed. Trying /videofeed …");
      img.src = b + "/videofeed";
    };
    img.onload = function () {
      setOn(true, "PHONE LIVE");
      $("wc-readout").textContent = "Showing phone IP Webcam. Cover the lens or walk in front of it.";
    };
    log("Opening " + b + "/video  (same Wi‑Fi required)");
    $("wc-readout").textContent = "Connecting to phone… if blank, allow insecure content or use Snapshots.";
    try { localStorage.setItem("ss_ipwebcam", b); } catch (e) {}
  }

  function showSnapshots() {
    const b = baseUrl();
    if (!b) { alert("Type the IP Webcam address first."); return; }
    stopAll();
    const img = $("wc-ipimg");
    img.style.display = "block";
    function tick() {
      img.src = b + "/shot.jpg?t=" + Date.now();
    }
    tick();
    shotTimer = setInterval(tick, 400);
    setOn(true, "PHONE SNAPSHOTS");
    log("Snapshot mode " + b + "/shot.jpg every 0.4s");
    $("wc-readout").textContent = "Refreshing still pictures from the phone.";
    try { localStorage.setItem("ss_ipwebcam", b); } catch (e) {}
  }

  async function startLaptop() {
    stopAll();
    try {
      stream = await navigator.mediaDevices.getUserMedia({ video: true, audio: false });
      const v = $("wc-video");
      v.classList.remove("hidden");
      v.srcObject = stream;
      await v.play();
      setOn(true, "LAPTOP");
      log("Laptop webcam ON.");
    } catch (err) {
      log("Laptop webcam failed: " + err.message);
      alert("Allow camera, or use the phone address instead.");
    }
  }

  window.WebcamTest = {
    onShow: function () {
      try {
        const a = $("wc-relay-link");
        const origin = location.hostname === "127.0.0.1" || location.hostname === "localhost"
          ? (location.protocol + "//172.29.156.12:" + location.port)
          : location.origin;
        if (a) a.textContent = origin + "/phone-send";
        const saved = localStorage.getItem("ss_ipwebcam");
        if (saved && $("wc-url")) $("wc-url").value = saved;
        showSaved();
      } catch (e) {}
      log("Auto-connecting to phone relay...");
      showRelay();
    },
    onHide: function () {},
  };

  document.addEventListener("click", function (e) {
    const t = e.target;
    if (!t) return;
    if (t.id === "wc-relay") showRelay();
    if (t.id === "wc-copy") {
      const u = ($("wc-relay-link") && $("wc-relay-link").textContent) || (location.origin + "/phone-send");
      if (navigator.clipboard && navigator.clipboard.writeText) {
        navigator.clipboard.writeText(u).then(function () { log("Copied: " + u); alert("Copied. Open this on the phone Chrome."); });
      } else {
        prompt("Copy this on the phone:", u);
      }
    }
    if (t.id === "wc-add") addLink();
    if (t.classList && t.classList.contains("wc-use")) {
      $("wc-url").value = t.getAttribute("data-url") || "";
      showPhoneVideo();
    }
    if (t.id === "wc-start") showPhoneVideo();
    if (t.id === "wc-shot") showSnapshots();
    if (t.id === "wc-stop") stopAll();
    if (t.id === "wc-laptop") startLaptop();
  });
})();
