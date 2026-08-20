import cv2
import urllib.request
import numpy as np

def get_live_frame(camera_num):
    # Try stream URL first
    stream_url = f"https://live.sentinelgujarat.in/stream/{camera_num}"
    try:
        cap = cv2.VideoCapture(stream_url)
        if cap.isOpened():
            ok, frame = cap.read()
            cap.release()
            if ok and frame is not None:
                return frame, "live_stream"
    except Exception:
        pass

    # Fallback to sample clip
    fallback_path = "media/demos/cam26_dhanori.mp4"
    cap = cv2.VideoCapture(fallback_path)
    if cap.isOpened():
        ok, frame = cap.read()
        cap.release()
        if ok and frame is not None:
            return frame, "sample_clip"
            
    return None, "none"

if __name__ == "__main__":
    frame, src = get_live_frame(8)
    print("Fetched frame for Camera 8:", frame.shape if frame is not None else None, "| Source:", src)
