import streamlit as st
from pytube import YouTube
import whisper
import os

st.title("🎙️ Chuyển giọng nói YouTube thành văn bản")

video_url = st.text_input("Dán link YouTube vào đây:")

if st.button("Chuyển đổi"):
    if not video_url:
        st.warning("Bạn chưa nhập URL!")
    else:
        st.info("🔽 Đang tải video...")
        yt = YouTube(video_url)
        audio_stream = yt.streams.filter(only_audio=True).first()
        audio_path = audio_stream.download(filename="audio.mp4")

        st.info("🧠 Đang chuyển giọng nói thành văn bản...")
        model = whisper.load_model("base")
        result = model.transcribe(audio_path)

        st.success("✅ Chuyển đổi xong!")
        st.text_area("📄 Văn bản:", result["text"], height=300)

        os.remove(audio_path)
