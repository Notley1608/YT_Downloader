from pytubefix import YouTube
import io

def get_video_info(url):
    """
    Given a YouTube URL, returns the video title and a list of available progressive streams.
    Each stream is represented as a dict with keys: itag, resolution, filesize_mb
    """
    yt = YouTube(url)
    streams = yt.streams.filter(progressive=True).order_by('resolution').desc()

    stream_list = []
    for stream in streams:
        stream_list.append({
            "itag": stream.itag,
            "resolution": stream.resolution,
            "filesize_mb": round(stream.filesize / (1024 * 1024), 2)
        })

    return yt.title, stream_list


def download_video(url, itag):
    """
    Download the YouTube video stream with the given itag from url.
    Returns bytes of the downloaded video file.
    """
    yt = YouTube(url, use_oauth=False, allow_oauth_cache=False)
    stream = yt.streams.get_by_itag(itag)
    if stream is None:
        raise ValueError("Stream with itag not found.")
    # Download to a bytes buffer
    buffer = io.BytesIO()
    stream.stream_to_buffer(buffer)
    buffer.seek(0)
    return buffer.read()