import nltk, spacy, spacy.cli, string, matplotlib.pyplot as plt

from nltk.corpus import stopwords
from nltk.sentiment import SentimentIntensityAnalyzer
from wordcloud import WordCloud

"""

Text analysis package.
It is a package generated to perform easy analysis on .txt files. 
It makes it easy to analyze texts through different tools and facilities like word counting, sentence splitting, sentiment analysis and so on.
Different packages like spicy or nltk have been used to facilitate the development of the tool and increase the output quality.

"""

class TXTanalyzer():

    def __init__(self, txt_file_path:str):
        self.text = self.__read_file(txt_file_path)
        if self.text == "":
            raise Exception("El fichero no puede estar vacío. Debe contener algún tipo de texto.")

    def __read_file(self, txt_file_path:str):
        self.txt_file_path = txt_file_path
        if txt_file_path.lower().endswith('.txt'):
            file = open(txt_file_path,"r")
            return file.read()
        else:
            raise Exception("El fichero debe tener extensión .txt.")
        
    def print_text(self):
        return self.text
    
    def sentence_splitting(self):
        try:
            self.nlp = spacy.load("en_core_web_sm")
        except OSError:
            # Model not found, download it
            print(f"Descargando modelo de separación de frases...")
            spacy.cli.download("en_core_web_sm")
            self.nlp = spacy.load("en_core_web_sm")
        finally:
            frases = self.nlp(self.text)
        return [sent.text for sent in frases.sents]
    
    def __remove_stopwords(self):
        cleaned_text = self.text.translate(str.maketrans('', '', string.punctuation))
        all_words = cleaned_text.split()
        stop_words = set(stopwords.words('spanish'))
        filtered_words = [word.replace('¿', '') for word in all_words if word.lower() not in stop_words] # el carácter '¿' no lo detecta la librería string por lo que aprovechamos para eliminarlo ahora
        return filtered_words
    
    def word_count(self):
        """
        Must consider that stopwords are previously removed.
        """
        try:
            self.words = self.__remove_stopwords()
        except OSError:
            # Model not found, download it
            print(f"Descargando modelo para eliminar stopwords...")
            nltk.download('stopwords')
            self.words = self.__remove_stopwords()
        total_chars = [char for char in self.text]
        return f"Word count: {len(self.words)}\nUnique word count: {len(set(self.words))}\nTotal characters: {len(total_chars)}"
    
    def word_freq(self):
        self.word_count()
        word_frequency = {}
        for word in self.words:
            word = word.lower()
            word_frequency[word] = word_frequency.get(word, 0) + 1
        return word_frequency
    
    def wordcloud(self):
        wordcloud = WordCloud().generate_from_frequencies(self.word_freq())
        plt.imshow(wordcloud, interpolation='bilinear')
        plt.axis("off")
        return plt.show()

if __name__ == "__main__":
    analyzer = TXTanalyzer('hola.txt')
    print(analyzer.wordcloud())



class TXTsummarizer(TXTanalyzer):
    pass