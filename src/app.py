import streamlit as st
from downloader import get_video_info, download_video

st.set_page_config(
    page_title="Youtube downloader",
    page_icon="🎬",
    layout="centered"
)
st.title("🎬 Youtube downloader")
st.caption("Download your favourite YouTube videos in high quality instantly.")

url = st.text_input("🔗 Paste YouTube video link here:", placeholder="https://youtube.com...")

if url:
    with st.spinner("🔍 Fetching video details..."):
        try:
            title, streams = get_video_info(url)
            
            with st.container(border=True):
                st.subheader("📺 Video Found")
                st.markdown(f"**Title:** `{title}`")
                
                options = [f"🎥 {s['resolution']} ({s['filesize_mb']} MB)" for s in streams]
                
                choice_index = st.selectbox(
                    "📥 Select your preferred quality:", 
                    list(range(len(streams))), 
                    format_func=lambda x: options[x]
                )
                
                if st.button("🚀 Process Video", use_container_width=True):
                    itag = streams[choice_index]['itag']
                    
                    with st.status("📥 Downloading from YouTube server...", expanded=True) as status:
                        video_bytes = download_video(url, itag)
                        status.update(label="✅ Video processed successfully!", state="complete", expanded=False)
                    
                    st.toast("Your download is ready!", icon="🎉")
                    
                    st.download_button(
                        label="💾 Save Video to Device",
                        data=video_bytes,
                        file_name=f"{title}.mp4",
                        mime="video/mp4",
                        type="primary",
                        use_container_width=True
                    )
                    
        except Exception as e:
            st.error(f"❌ Failed to load video. Error: {e}")
