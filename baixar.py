import streamlit as st
import yt_dlp
import os
from datetime import datetime
import tempfile

st.set_page_config(page_title="📥 Baixador de Vídeos", layout="centered")

st.title("📹 Baixador de Vídeos do YouTube ou Vídeo Local")

modo = st.radio("Selecione o modo:", ["Baixar do YouTube", "Usar vídeo local"])

if modo == "Baixar do YouTube":
    url = st.text_input("Cole a URL do vídeo do YouTube")

    if st.button("🔽 Baixar vídeo"):
        if not url:
            st.warning("Por favor, informe a URL.")
        else:
            try:
                # Diretório temporário
                temp_dir = tempfile.mkdtemp()
                data_hora = datetime.now().strftime("_%Y-%m-%d-%H-%M")
                output_template = os.path.join(temp_dir, f'%(title)s{data_hora}.%(ext)s')

                ydl_opts = {
                    'outtmpl': output_template,
                    'quiet': True,
                }

                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    info = ydl.extract_info(url, download=True)
                    titulo = info.get('title', 'video')
                    ext = info.get('ext', 'mp4')
                    file_path = os.path.join(temp_dir, f"{titulo}{data_hora}.{ext}")

                with open(file_path, "rb") as f:
                    st.success("Download concluído!")
                    st.download_button(
                        label="📥 Clique para baixar o vídeo",
                        data=f,
                        file_name=os.path.basename(file_path),
                        mime="video/mp4"
                    )
            except Exception as e:
                st.error(f"Erro: {str(e)}")

else:
    video_file = st.file_uploader("📁 Envie um vídeo local", type=["mp4", "mov", "mkv", "avi"])
    if video_file:
        st.video(video_file)
        st.download_button(
            label="📥 Baixar cópia do vídeo enviado",
            data=video_file,
            file_name=video_file.name,
            mime="video/mp4"
        )
