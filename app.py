import streamlit as st
import whisper
import yt_dlp
import os
import tempfile

st.set_page_config(page_title="YouTube Voice to Text", layout="centered")

st.title("🎧 Chuyển giọng nói từ YouTube thành văn bản")
url = st.text_input("🔗 Dán link YouTube ở đây:")

if st.button("🎬 Chuyển đổi"):
    if not url:
        st.warning("⚠️ Bạn cần nhập link video YouTube.")
        st.stop()

    with st.spinner("🔊 Đang tải và xử lý âm thanh..."):
        # Tạo file tạm
        with tempfile.TemporaryDirectory() as tmpdir:
            audio_path = os.path.join(tmpdir, "audio.mp3")

            # Cấu hình yt-dlp để tải audio
            ydl_opts = {
                "format": "bestaudio/best",
                "outtmpl": audio_path,
                "quiet": True,
                "postprocessors": [{
                    "key": "FFmpegExtractAudio",
                    "preferredcodec": "mp3",
                    "preferredquality": "192",
                }],
            }

            try:
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    ydl.download([url])
            except Exception as e:
                st.error(f"❌ Lỗi khi tải video: {e}")
                st.stop()

            # Load mô hình Whisper và phiên âm
            try:
                model = whisper.load_model("base")
                result = model.transcribe(audio_path)
                st.success("✅ Hoàn tất!")
                st.subheader("📄 Văn bản:")
                st.write(result["text"])
            except Exception as e:
                st.error(f"❌ Lỗi khi chuyển âm thanh thành văn bản: {e}")
