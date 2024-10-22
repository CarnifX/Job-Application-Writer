import PyPDF2
import docx2txt
import requests
from bs4 import BeautifulSoup

#Funksjonen henter ut tekst fra en PDF-fil, som i dette tilfellet inneholder en CV.
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