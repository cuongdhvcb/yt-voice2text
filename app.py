import streamlit as st
from pytube import YouTube
from moviepy.editor import VideoFileClip
import whisper, os, uuid, tempfile

st.title("🎙️ YouTube → Văn bản")

url = st.text_input("🔗 Dán link YouTube ở đây:")
run_btn = st.button("Chuyển đổi")

def download_audio(y_url):
    yt = YouTube(y_url)
    stream = yt.streams.filter(only_audio=True).first()
    return stream.download(filename=f"{uuid.uuid4().hex}.mp4")

def extract_wav(mp4_path):
    wav_path = tempfile.mktemp(suffix=".wav")
    VideoFileClip(mp4_path).audio.write_audiofile(wav_path)
    return wav_path

def transcribe(wav_path):
    model = whisper.load_model("base")   # Có thể đổi thành 'tiny' nếu máy yếu
    out = model.transcribe(wav_path)
    return out["text"]

if run_btn and url:
    try:
        with st.spinner("⬇️ Đang tải..."):
            mp4_path = download_audio(url)
        with st.spinner("🎧 Tách âm thanh..."):
            wav_path = extract_wav(mp4_path)
        with st.spinner("🧠 Nhận diện giọng nói..."):
            text = transcribe(wav_path)
        st.success("✅ Hoàn tất!")
        st.text_area("📄 Văn bản:", text, height=300)
    except Exception as e:
        st.error(f"Lỗi: {e}")


