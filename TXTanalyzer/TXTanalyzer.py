import nltk, spacy, spacy.cli, string, matplotlib.pyplot as plt, math
from nltk import sent_tokenize, word_tokenize, PorterStemmer
from nltk.corpus import stopwords
from nltk.sentiment import SentimentIntensityAnalyzer
from wordcloud import WordCloud

"""
Librería de análisis de texto.
Es una librería generada para realizar un análisis sencillo de archivos .txt
Facilita el análisis de textos a través de diversas herramientas y facilidades, como el conteo de palabras, la división de oraciones, el análisis de sentimientos y más.
Se han utilizado diferentes librerías como spaCy o nltk para facilitar el desarrollo de la herramienta y mejorar la calidad de los resultados.
"""

class TXTanalyzer:

    def __init__(self, txt_file_path:str):
        """
        Constructor de la clase. Lee el contenido de un archivo de texto especificado y lo almacena en el objeto.

        Args:
            txt_file_path (str): La ruta al archivo de texto a leer.

        Raises:
            Exception: Se lanza una excepción si el archivo está vacío.
        """
        self.text = self.read_file(txt_file_path)
        if self.text == "":
            raise Exception("El fichero no puede estar vacío. Debe contener algún tipo de texto.")

    def read_file(self, txt_file_path:str):
        """
        Lee el contenido de un archivo de texto y lo devuelve como una cadena de texto.

        Args:
            txt_file_path (str): La ruta al archivo de texto a leer.

        Returns:
            str: El contenido del archivo como una cadena de texto.

        Raises:
            Exception: Se lanza una excepción si el archivo no tiene una extensión .txt
        """
        self.txt_file_path = txt_file_path
        if txt_file_path.lower().endswith('.txt'):
            file = open(txt_file_path,"r")
            return file.read()
        else:
            raise Exception("El fichero debe tener extensión .txt")
        
    def print_text(self):
        """
        Devuelve el texto almacenado en el objeto.

        Returns:
            str: El texto almacenado en el objeto como una cadena de texto.
        """
        return self.text
    
    def sentence_splitting(self):
        """
        Divide el texto en frases utilizando el modelo de lenguaje "en_core_web_sm" de SpaCy.

        Returns:
            list: Una lista de frases obtenidas a partir del texto.
        """
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
        """
        Elimina las palabras vacías (stopwords) y signos de puntuación del texto.

        Returns:
            list: Una lista de palabras del texto después de eliminar stopwords y puntuación.
        """
        cleaned_text = self.text.translate(str.maketrans('', '', string.punctuation))
        all_words = cleaned_text.split()
        stop_words = set(stopwords.words('spanish'))
        filtered_words = [word.replace('¿', '') for word in all_words if word.lower() not in stop_words] # el carácter '¿' no lo detecta la librería string por lo que aprovechamos para eliminarlo ahora
        return filtered_words
    
    def word_count(self):
        """
        Procesa el texto para calcular estadísticas, incluyendo el recuento de palabras, el recuento de palabras únicas y
        el recuento total de caracteres. Las 'stopwords' son previamente eliminadas.

        Returns:
            str: Un string que contiene las estadísticas de procesamiento del texto.
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
        """
        Calcula la frecuencia de las palabras en el texto y devuelve un diccionario que asocia cada palabra
        con su frecuencia.

        Returns:
            dict: Un diccionario que contiene las palabras como claves y sus frecuencias como valores.
        """
        self.word_count()
        word_frequency = {}
        for word in self.words:
            word = word.lower()
            word_frequency[word] = word_frequency.get(word, 0) + 1
        return word_frequency
    
    def wordcloud(self):
        """
        Crea y muestra una representación de nube de palabras basada en la frecuencia de las palabras en el texto.

        Returns:
            None
        """
        wordcloud = WordCloud().generate_from_frequencies(self.word_freq())
        plt.imshow(wordcloud, interpolation='bilinear')
        plt.axis("off")
        return plt.show()
    
    def sia(self):
        """
        Realiza un análisis de sentimiento (SIA - Sentiment Intensity Analyzer) en el texto y devuelve los resultados.

        Returns:
            str: Un string que contiene la negatividad, neutralidad y positividad del texto.
        """
        sia = SentimentIntensityAnalyzer().polarity_scores(self.text)
        neg, neu, pos = sia['neg'], sia['neu'], sia['pos']
        return f"Negativity: {neg}\nNeutrality: {neu}\nPositivity: {pos}"
    
