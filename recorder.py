import pyaudio
import wave
from threading import Event

#bu metoda sıradan bir veri yapısı değil threadlerle ilgili bi ozellık gelecek cunku streamlıt multı threadıng e ızın vermıyor
"""'while loop' kullanımını düzenle: Sürekli okuma yapmasını engellemek için 'recorder' modülünde 'while loop' şartını düzelt.
'isRecordingActive' değişkeni ekle: Ses kaydını 'stop' butonu ile durdurmak için 'isRecordingActive' adında bir değişken tanımla.
'multi-threading' kullanımını uygula: Ses kaydının kesintisiz devam etmesi ve diğer işlemlerin eş zamanlı yürütülmesi için 'multi-threading' yaklaşımını benimse.
app.py bileşeni ve yeni 'thread': app.py adlı merkezi bir bileşen oluştur ve kayıt işlemini bu bileşenin içindeki yeni bir 'thread' üzerinden yürüt"""


def record(record_active, frames):
    audio = pyaudio.PyAudio() #pyaudionun metodlarına ve ozellıklerıne audıo sınıfı uzerınden ulasacagız

 #ses işleme için bir stream nesnesi olusturalım kayıdın basından sonuna kadar kaydedecegımız yapı
    stream = audio.open(
        format=pyaudio.paInt16,  #16 bit ses formatı paInt16
        channels=1,   #monochannel
        rate=44100,   #yuksek kalıtelı ses kaydı ıcın gereklı frekans
        input=True,   #stream ıcındekı verılerı bı yere gonderme bızım ıstedıgımız yere kaydet
        frames_per_buffer=1024  #bir defada 1024 frame alabılelım kayıt esnasında
    ) 

    while record_active.is_set():     #kayıt döngüsü süreklilik arz ettıgı ıcın whıle dongusune ıhtıyacımız var
        data = stream.read(1024, exception_on_overflow=False)  #exception_on_overflow=False, ara bellege yanı buffera alma sırasında olur da bir overflow olursa hata vermez surec kesılmez, data nesnesıne kayıtlarımızı topluyoruz
        frames.append(data) #sonrasında datayı frames adında bir listeye ekliyoruz ama  henuz frames tanımlı degıl cunku bu lıstede tıpkı record active gibi bize dısardan gelecek cunku kaydettıgımız verılerı sessıon statede tutuyoruz her defasında bastan baslamasın istediğimiz için ve parametrelere framesi de ekliyoruz

 #record active set edılsıyse whıle dongusu calısmaya baslayacak, durması içinse thread in başladığı app.py dosyası ıcerısınde durduruyor olacagız, multithreading sayesınde olan bı durum bu

    
    stream.stop_stream() #kayıtı durdur
    stream.close() #kapatlım kı bellekte yer tutmaya devam etmesin
    audio.terminate() 
 #katıt alma işimiz bitti sırada yerelde dosyaya kaydetmelıyız


    sound_file = wave.open("voice_prompt.wav", "wb") #dosyanın nereye kaydedılecegını ve formatını girdik
    sound_file.setnchannels(1) #monochannel
    sound_file.setsampwidth(audio.get_sample_size(pyaudio.paInt16)) #orneklem buyuklugu 
    sound_file.setframerate(44100) #hz
    sound_file.writeframes(b''.join(frames)) #bu frameleri nereye yazacagız,bu lıstenın her bır elemanını bırbırı ardına joınleyıo tek bır stringe cevirdik gibi düşüeniliriz
    sound_file.close() #dosyayı kapat arıza cıkmasın 

 #streamlit için ses kaydeden bılesenımız hazırrrrr sırada sesı metne cevıren transkriptorı yazmak var

















"""
def record(record_active, frames):
    audio = pyaudio.PyAudio()

    stream = audio.open(
        format=pyaudio.paInt16,
        channels=1,
        rate=44100,
        input=True,
        frames_per_buffer=1024
    )

    while record_active.is_set():
        data = stream.read(1024, exception_on_overflow=False)
        frames.append(data)

    stream.stop_stream()
    stream.close()
    audio.terminate()

    sound_file = wave.open("voice_prompt.wav", "wb")
    sound_file.setnchannels(1)
    sound_file.setsampwidth(audio.get_sample_size(pyaudio.paInt16))
    sound_file.setframerate(44100)
    sound_file.writeframes(b''.join(frames))
    sound_file.close()"""




