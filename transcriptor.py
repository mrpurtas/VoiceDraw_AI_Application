from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()

my_key_openai= os.getenv("openai_apikey")

client = OpenAI(
    api_key=my_key_openai
)

#openai a api cagrısı yapmaya hazırız 

def transcribe_with_whisper(audio_file_name):
    audio_file = open(audio_file_name, "rb") #dosyamzı audio_file içerisine tasımıs olduk

    AI_generated_transcript = client.audio.transcriptions.create(
        model ="whisper-1",
        file=audio_file,
        language="tr"
    )

    return AI_generated_transcript.text

#whisperı api bazlı degıl yerele kurarak bedavaya kullanabılırız
#FFMPEg kurulur(chocolatey ıle kurulur), acık kaynak whısper baska bı yerden cekılıp bılıgsayara kurulur ona ayrılacak hard dsık space ayırılmalı, base model kullanılır muhtemelen bu yuzden ama base model apıdekınden cok daha kotu calısır.