import os #readfile
import textract #pdftotext
import spacy #import library
import re
import spacy_streamlit
import typer
import nltk
from nltk.tokenize import RegexpTokenizer
from nltk.corpus import stopwords
from spacy.tokens import Doc, DocBin

def convertpdfstotext(path):
    filelist = []

    for fp in os.listdir(path):
        allfiles = filelist.append(os.path.join(path, fp))

    for f in filelist:
        doc = textract.process(f)
    return doc

# path = r'C:\Users\shali\OneDrive\Desktop\wiki\Terminology\Terminology_project\Data'
path = r'/mnt/c/Users/shali/OneDrive/Desktop/wiki/Terminology/Terminology_project/Data'
output_path = r'/mnt/c/Users/shali/OneDrive/Desktop/wiki/Terminology/Terminology_project/output/output.txt'
doc = convertpdfstotext(path)
# print(doc)

def preprocessing(convertpdftotext):
    text = doc.decode('utf8') #convert to byte
    removing = text.replace('\n','') #remove the production of textract
    removing = text.replace('\r','') #remove the production of extract
    sentence=str(removing)
    sentence=sentence.replace('{html}',"")
    cleanr = re.compile('<.*?>')
    cleantext = re.sub(cleanr, '', sentence)
    rem_url=re.sub(r'http\S+', '',cleantext)
    rem_num = re.sub('[0-9]+', '', rem_url)
    tokenizer = RegexpTokenizer(r'\w+')
    tokens = tokenizer.tokenize(rem_num)
    filtered_words = [w for w in tokens if len(w) > 2 if not w in stopwords.words('english')]
    referenceremoval = text.partition("References")[0]
    return " ".join(filtered_words)

cleandata = preprocessing(doc)
# print(cleandata)

def model_visualize(models: str, default_text: str):
    models = [name.strip() for name in models.split(",")]
    spacy_streamlit.visualize(models, default_text, visualizers=["ner"])

nlp = spacy.load('en_core_web_sm')
#load model which is sm small model and en means english
data = nlp(cleandata)
# print(data)
# print(type(data))

nlp = spacy.blank("en")
doc_bin = DocBin(attrs=["ENT_IOB"])
doc_bin.add(data)
doc_bin.to_disk("./train.spacy")
typer.run(model_visualize)
print(f"Processed {len(doc_bin)}")


