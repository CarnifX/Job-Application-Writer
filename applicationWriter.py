from dotenv import load_dotenv
import html2text
from openai import OpenAI
from utility_functions import*

#Oppretter tre strings: en for CV(curriculum_vitae) fra pdf, en for CV(curriculum_vitae) fra docx,
#og en for annonseteksten(text_content). Har planer om å implementere drag 'n drop av filer senere,
#hvor koden gjennkjenner filtypen og bruker den funksjonen som passer.
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