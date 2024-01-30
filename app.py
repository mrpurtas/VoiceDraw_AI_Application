import streamlit as st
import threading  #Ses kaydetme sürecinin kesinti olmaksızın devam eden bir veri akışına ihtiyaç duyduğunu ve streamlit her bir etkileşimde sayfayı yenilediği için bu veri akışının bozulduğunu biliyoruz dolayısıyla buna çare olarak da threadingden faydalanacağız yani farklı iş parçalarını işlemcinin farklı bölümlerine havale ederek eşzamanlı olarak işletilmesini sağlayacağız 
import recorder
import transcriptor
import painter
import datetime

#export PATH="/opt/homebrew/bin:$PATH"


if "record_active" not in st.session_state:
    st.session_state.record_active = threading.Event()
    st.session_state.recording_status = "Başlamaya Hazırız!"
    st.session_state.recording_completed = False
    st.session_state.latest_image = ""
    st.session_state.messages = []
    st.session_state.frames = []

def start_recording():   #ses kaydı baslatılsın dedıgımızde neler olmalı
    st.session_state.record_active.set() #bır threadin baslayıp baslamadıgını yorumlayıcımız bılecek .set sayesınde
    st.session_state.frames.clear()
    st.session_state.recording_status = "🔴  **Sesiniz Kaydediliyor...**"
    st.session_state.recording_completed = False

    frames = st.session_state.frames
    threading.Thread(target=recorder.record, args=(st.session_state.record_active, frames)).start()    #her başlat butonuna tıklandığında bu thread başlayacak ve bütün kayıt işlemleri ayrı bir işlem parçası olarak streamlette yaşanan kesintilerden etkilenmeden yoluna devam edecek, start metodunu çağırıyoruz bu start metodunu çağırdımız noktada gerçekten yeni bir thread açılıyor ve işlemcisi streamlitin diğer yaptığı işlerden bağımsız olarak bu trade altındaki record metodunu yürütmeye devam ediyor.


def stop_recording():
    st.session_state.record_active.clear()
    st.session_state.recording_status = "✅  **Kayıt Tamamlandı**"
    st.session_state.recording_completed = True



st.set_page_config(page_title="VoiceDraw", layout="wide", page_icon="./icons/app_icon.png")
st.image(image="./icons/top_banner.png", use_column_width=True)
st.title("VoiceDraw: Sesli Çizim")
st.divider()

col_audio, col_image = st.columns([1,4]) #1e 4 bolduk genıslıklerı 

with col_audio:
    st.subheader("Ses Kaydı")
    st.divider()
    status_message = st.info(st.session_state.recording_status) #ses kaydı devam ediyor mu etmıyor mu u st info widgetla gosterıyoruz
    st.divider()

    subcol_left, subcol_right = st.columns([1,2])

    with subcol_left:
        start_btn = st.button(label="Başlat", on_click=start_recording, disabled=st.session_state.record_active.is_set()) #kayıt basladıysa start butonumuz dısabled olsun 
        stop_btn = st.button(label="Durdur", on_click=stop_recording, disabled = not st.session_state.record_active.is_set())
    with subcol_right:
        recorded_audio = st.empty()

        if st.session_state.recording_completed:
            recorded_audio.audio(data="voice_prompt.wav")

    st.divider()
    latest_image_use = st.checkbox(label="Son Resmi Kullan")

with col_image:
    st.subheader("Görsel Çıktılar")
    st.divider()

    for message in st.session_state.messages:
        if message["role"] == "assistant":
            with st.chat_message(name=message["role"], avatar="./icons/ai_avatar.png"):
                st.warning("İşte Sizin İçin Oluşturduğum Görsel:")
                st.image(message["content"], width=300)
        elif message["role"] == "user":
            with st.chat_message(name=message["role"], avatar="./icons/user_avatar.png"):
                st.success(message["content"])
    if stop_btn:
        with st.chat_message(name="user", avatar="./icons/user_avatar.png"):
            with st.spinner("Sesiniz Çözümleniyor..."):
                voice_prompt = transcriptor.transcribe_with_whisper(audio_file_name="voice_prompt.wav")
            st.success(voice_prompt)

    # if stop_btn:
    #     with st.chat_message(name="user", avatar="./icons/user_avatar.png"):
    #         with st.spinner("Sesiniz Çözümleniyor..."):
    #             voice_prompt = transcriptor.transcribe_with_whisper(audio_file_name="voice_prompt.wav")
    #         st.success(voice_prompt)

        st.session_state.messages.append({"role": "user", "content": voice_prompt})

        with st.chat_message(name="assistant", avatar="./icons/ai_avatar.png"):
            st.warning("İşte Sizin İçin Oluşturduğum Görsel:")
            with st.spinner("Görseliniz Oluşturuluyor..."):
                if latest_image_use:
                    image_file_name = painter.generate_image(image_path=st.session_state.latest_image, prompt=voice_prompt)
                else:
                    image_file_name = painter.generate_image_with_dalle(prompt=voice_prompt)
    
            st.image(image=image_file_name, width=300)

            with open(image_file_name, "rb") as file:
                st.download_button(
                    label="Resmi İndir",
                    data=file,
                    file_name=image_file_name,
                    mime="image/png"
                )

    
        st.session_state.messages.append({"role": "assistant", "content": image_file_name})
        st.session_state.latest_image = image_file_name
