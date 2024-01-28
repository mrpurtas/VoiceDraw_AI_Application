import google.generativeai as genai
import PIL.Image
import requests
import os
from dotenv import load_dotenv
from openai import OpenAI
from io import BytesIO
from datetime import datetime



load_dotenv()

my_key_openai= os.getenv("openai_apikey")

client = OpenAI(
    api_key=my_key_openai
)


def generate_image_with_dalle(prompt):
        
    AI_Response = client.images.generate(
    model="dall-e-3",
    size ="1024x1024",
    quality= "hd",
    n=1,
    response_format="url", #yanıtı dogrudan resım verısı olarak ıstedıgımızde sorunlar olabılıyor o yuzden sonradan urlı gorsele donsutureblecegız
    prompt=prompt
    )
    image_url = AI_Response.data[0].url

    response = requests.get(image_url)
    image_bytes = BytesIO(response.content) #requests uzerınden ilgili donuslerı image_bytes'a depoladık

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"./img/generated_image_{timestamp}.png"

    if not os.path.exists("./img"): #ımg ismine sahip dızın halı hazırda yoksa olusturan kod parcaıgı
        os.makedirs("./img") #dizin olustur
     
    with open(filename, "wb") as file:
        file.write(image_bytes.getbuffer()) #dosyaya yazılan byteları gecıcı sure ile tutabılmek ıcın getbuffer kullandık
    
    return filename



#sırada coklu form var 

my_key_google= os.getenv("google_apikey")

client = OpenAI(
    api_key=my_key_openai
)
genai.configure(
    api_key=my_key_google
)

def gemini_vision_with_local_file(image_path, prompt):  #image_path resım adresı 

    multimodality_prompt = f"""Bu resmi, verdiğim ek yönergelerle detaylıca tarif edip yeniden yaratmanı istiyorum. İlk adım olarak, resmin ayrıntılarını net ve eksiksiz bir şekilde açıkla. Bu betimleme, yapay zeka modeli kullanılarak yeni bir görsel yaratmak için temel alınacak. Dolayısıyla, betimlemenin son hali, bir yapay zeka modeli tarafından işlenebilecek bir prompt olarak dikkate alınmalıdır. Ek yönergeler şunlardır: {prompt}
    """

    client = genai.GenerativeModel(model_name="gemini-pro-vision")

    source_image = PIL.Image.open(image_path) #adresten gelen kaynak resmı source ımage altında saklıyoruz

    AI_Response = client.generate_content(
        [
            multimodality_prompt,
            source_image
        ]
    )

    AI_Response.resolve()  #karsı taraftakı resım ıslemlerının bıttıgınden emın olmamızı saglıyo

    return AI_Response.text  #elımızde hala bı metın var bu bır gorsel uretme promptu


def generate_image(image_path, prompt):

    image_based_prompt = gemini_vision_with_local_file(image_path=image_path, prompt=prompt)

    filename = generate_image_with_dalle(prompt=image_based_prompt)

    return filename

"""Bu gönderdiğim resmi, bazı ek yönergelerle birlikte yeniden oluşturmanı istiyorum. Bunun için ilk olarak resmi son derece ayrıntılı biçimde betimle. Daha sonra sonucunda bana vereceğin metni, bir yapay zeka modelini kullanarak görsel oluşturmaktaki kullanacağım. O yüzden yaptığın son halini verirken bunun resmi üretmekte kullanılacak bir girdi yani prompt olduğunu dikkate al. İşte ek yönerge şöyle: {prompt}"""

"""multimodality_prompt = Yeniden oluşturulmasını istediğim resmi, eklediğim özel yönergeler doğrultusunda son derece ayrıntılı ve dikkatli bir şekilde tarif etmeni rica ediyorum. Bu tarifi, yapay zeka modelini kullanarak görsel üretim sürecinde bir girdi olarak kullanacağım. Bu nedenle, vereceğin son betimlemenin bir yapay zeka modeli tarafından görsel oluşturmak için kullanılacak bir prompt olarak işlev göreceğini unutma. İşte ek yönerge: {prompt}
    """


""" Bu resmi, verdiğim ek yönergelerle detaylıca tarif edip yeniden yaratmanı istiyorum. İlk adım olarak, resmin ayrıntılarını net ve eksiksiz bir şekilde açıkla. Bu betimleme, yapay zeka modeli kullanılarak yeni bir görsel yaratmak için temel alınacak. Dolayısıyla, betimlemenin son hali, bir yapay zeka modeli tarafından işlenebilecek bir prompt olarak dikkate alınmalıdır. Ek yönergeler şunlardır: {prompt}
    """


"""class Painter:
    def __init__(self):
        self.my_key_openai = os.getenv("openai_apikey")
        self.my_key_google = os.getenv("google_apikey")

        # OpenAI ve GenAI için API anahtarlarını yapılandırma
        self.openai_client = OpenAI(api_key=self.my_key_openai)
        genai.configure(api_key=self.my_key_google)

    def generate_image_with_dalle(self, prompt):
        AI_Response = self.openai_client.images.generate(
            model="dall-e-3",
            size="1024x1024",
            quality="hd",
            n=1,
            response_format="url",
            prompt=prompt
        )
        image_url = AI_Response.data[0].url

        response = requests.get(image_url)
        image_bytes = BytesIO(response.content)

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"./img/generated_image_{timestamp}.png"

        if not os.path.exists("./img"):
            os.makedirs("./img")
        
        with open(filename, "wb") as file:
            file.write(image_bytes.getbuffer())
        
        return filename

    def gemini_vision_with_local_file(self, image_path, prompt):
        multimodality_prompt = f""Bu gönderdiğim resmi, bazı ek yönergelerle birlikte yeniden oluşturmanı istiyorum. Bunun için ilk olarak resmi son derece ayrıntılı biçimde betimle. Daha sonra sonucunda bana vereceğin metni, bir yapay zeka modelini kullanarak görsel oluşturmaktaki kullanacağım. O yüzden yaptığın son halini verirken bunun resmi üretmekte kullanılacak bir girdi yani prompt olduğunu dikkate al. İşte ek yönerge şöyle: {prompt}
        ""

        client = genai.GenerativeModel(model_name="gemini-pro-vision")

        source_image = PIL.Image.open(image_path)

        AI_Response = client.generate_content(
            [
                multimodality_prompt,
                source_image
            ]
        )

        AI_Response.resolve()
        return AI_Response.text

    def generate_image(self, image_path, prompt):
        image_based_prompt = self.gemini_vision_with_local_file(image_path=image_path, prompt=prompt)
        filename = self.generate_image_with_dalle(prompt=image_based_prompt)
        return filename"""


"""Bu yapılandırmada, öncelikle Painter sınıfının bir __init__ yapıcı fonksiyonu tanımlanmış ve API anahtarları bu fonksiyon içerisinde alınmıştır. Daha sonra, generate_image_with_dalle, gemini_vision_with_local_file ve generate_image fonksiyonları sınıf metodları olarak tanımlanmıştır. Her metod içerisindeki self kelimesi, sınıfın örneği üzerinden ilgili değişkenlere ve metodlara erişimi sağlar. Bu yapı sayesinde kodun okunabilirliği ve yönetimi kolaylaşır.

"""




"""Bir fantastik ormanın derinliklerinde, gizemli ve büyülü bir atmosferde, ışıkla dolu bir açıklıkta duran devasa bir ağaç. Bu ağaç, renkli kristallerle dolu dallara sahip ve etrafını saran parlak, neon renkli kelebeklerle çevrili. Ağacın altında, elinde büyülü bir asa tutan, uzun beyaz saçlı ve gümüş zırh giymiş bir elf kadını duruyor. Arkasında, uçan ejderhalar ve yüzen adalar görülüyor"""



"""yukarıda tanımlanan fantastik orman sahnesine bazı eklemeler yaparak görseli daha etkileyici hale getir. Devasa ağacın dallarında şimdi parlak mavi ve yeşil tonlarda ışıldayan, büyülü meyveler var. Elf kadının yanında, parlak turuncu renkli, ateşten kanatları olan bir phoenix kuşu duruyor. Arka planda, gökyüzünde dolunayın altında, kristal bir şato görünüyor. Ayrıca, elf kadının etrafında dönen küçük, ışık saçan peri topluluğu eklenmiş"""