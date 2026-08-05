import io
import traceback
from pytubefix import YouTube

def download_video(url, itag):
    print(f"[DOWNLOAD] URL: {url}")
    print(f"[DOWNLOAD] Requested itag: {itag}")

    try:
        print("[DOWNLOAD] Creating YouTube object...")
        yt = YouTube(url)
        print("[DOWNLOAD] YouTube object created.")

        print("[DOWNLOAD] Looking up stream...")
        stream = yt.streams.get_by_itag(itag)

        if stream is None:
            print("[DOWNLOAD] Stream not found.")
            raise ValueError("Stream with itag not found.")

        print(f"[DOWNLOAD] Stream found: {stream}")

        print("[DOWNLOAD] Downloading to buffer...")
        buffer = io.BytesIO()
        stream.stream_to_buffer(buffer)
        print("[DOWNLOAD] Download complete.")

        buffer.seek(0)
        data = buffer.read()
        print(f"[DOWNLOAD] Read {len(data)} bytes.")

        return data

    except Exception as e:
        print(f"[DOWNLOAD] ERROR: {type(e).__name__}: {e}")
        traceback.print_exc()
        raise