from nltk.stem import PorterStemmer
from bs4 import BeautifulSoup
from nltk.corpus import stopwords
from nltk.tokenize import wordpunct_tokenize
import re

ps = PorterStemmer()
stop_words = set(stopwords.words('english'))


def sentence_breakdown(text: str) -> list:
    # num_pattern = r'[0-9]'

    splitted_str = text.split()
    result = []
    for word in splitted_str:
        removed_special_char = re.sub('[^A-Za-z]+', '', word)
        # removed_number = re.sub(num_pattern, '', removed_special_char)
        tokenized = wordpunct_tokenize(removed_special_char)
        lowercase = tokenized.lower()
        if lowercase not in stop_words:
            stemmed = ps.stem(lowercase)
            result.append(stemmed)
        
    return result
    


def text_cleaner(html: str):
    soup = BeautifulSoup(html, features="html.parser")
    for script in soup(["script", "style"]):
        script.extract()    # rip it out
    # get text
    text = soup.get_text()

    # break into lines and remove leading and trailing space on each
    lines = [line.strip() for line in text.splitlines()]

    # break multi-headlines into a line each
    chunks = [phrase.strip() for line in lines for phrase in line.split("  ")]

    text = []
    for sentence in chunks:
        if sentence:
            text = text + sentence_breakdown(sentence)
            
    return text
