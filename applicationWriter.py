from bs4 import BeautifulSoup
from dotenv import load_dotenv
import requests
import html2text
from openai import OpenAI
import PyPDF2
import docx2txt


#Funksjonen henter ut text fra PDF-filen, som i dette tilfellet inneholder en CV.
def text_from_pdf(pdf_file):
    with open(pdf_file, "rb") as f:
        pdf = PyPDF2.PdfReader(f)
        text = ""
        for page in pdf.pages:
            text = text + page.extract_text() + " "
        return text


#Enkel funksjon som returnerer en string med docx tekst.
def text_from_docx(docx_file):
    return docx2txt.process(docx_file)


#Funksjonen web scraper tekst fra jobbannonse hentet fra
#"import-decoration' i html koden til en finn.no link.
#Det er her selve jobbeksrivelsen ligger
def get_text_from_web_link(web_address):

    page_to_scrape = requests.get(web_address)
    soup = BeautifulSoup(page_to_scrape.text, "html.parser")
    return str(soup.findAll("div", attrs={"class": "import-decoration"}))

#Enkel funksjon som åpner en tekstfil lagret i repertoaret,
#skriver inn stringen som kommer in som argument, og lukker filen
def write_to_txt_file(text):
    cover_letter_file = open("cover_letter.txt", "w")
    cover_letter_file.write(text)
    cover_letter_file.close()


#Oppretter tre strings: en for CV(curriculum_vitae) fra pdf, en for CV(curriculum_vitae) fra docx,
#og en for annonseteksten(text_content).
curriculum_vitae_pdf = text_from_pdf("ITCV-Odd-Jørgen-Frydendahl.pdf")
curriculum_vitae_docx = text_from_docx("ITCV-Odd-Jørgen-Frydendahl.docx")
raw_html_code = get_text_from_web_link("https://www.finn.no/job/fulltime/ad.html?finnkode=375482229")
text_content = html2text.html2text(raw_html_code)

#Henter ut API-nøkkel for chatGPT, lagret i en environment variable fil:
load_dotenv()
client = OpenAI()

#Sender prompt til ChatGPT, modell 3.5-turbo, hvor jeg sier at AIen skal
#oppføre seg som en jobbsøker med min CV, og skrive søketekst basert på
#finn.no info. Resultatet blir lagret i variabelen "completion".
completion = client.chat.completions.create(
    model = "gpt-3.5-turbo",
    messages=[
        {"role": "system", "content": "Du er en jobbsøker med denne CV'n: " + curriculum_vitae_docx},
        {"role": "user", "content": "Kan du skrive en jobbsøknad basert på CV'n du har, og denne jobbannonsen: " + text_content}
    ]
)

#Omgjør reslutatet fra ChatGPT til string, og lagrer teksten i en tekstfil.
final_text = str(completion.choices[0].message.content)
write_to_txt_file(final_text)