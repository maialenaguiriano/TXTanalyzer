import nltk, spacy, spacy.cli, string, matplotlib.pyplot as plt, math
from nltk import sent_tokenize, word_tokenize, PorterStemmer
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
        self.text = self.read_file(txt_file_path)
        if self.text == "":
            raise Exception("El fichero no puede estar vacío. Debe contener algún tipo de texto.")

    def read_file(self, txt_file_path:str):
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
    
    def sia(self):
        """
        SIA stands for Sentiment Intensity Analyzer
        """
        sia = SentimentIntensityAnalyzer().polarity_scores(self.text)
        neg, neu, pos = sia['neg'], sia['neu'], sia['pos']
        return f"Negativity: {neg}\nNeutrality: {neu}\nPositivity: {pos}"
    
class TXTsummarizer(TXTanalyzer):
    def __init__(self, txt_file_path:str):
        super().__init__(txt_file_path)
        self.text = self.read_file(txt_file_path)
        if self.text == "":
            raise Exception("El fichero no puede estar vacío. Debe contener algún tipo de texto.")
        
        self.summ = self.__procesar_texto()
        # 1. Tokenizar
        self.sentences = sent_tokenize(self.summ)
        self.total_documents = len(self.sentences)
        # 2. Crear matriz de frecuencias
        self.freq_matrix = self.__create_frequency_matrix() #divide por palabras cada frase y calcula la frecuencia en la que aparecen POR FRASE
        # 3. Calcular TermFrequency y generar matriz
        self.tf_matrix = self.__create_tf_matrix() #probabilidad por la que se repite cada palabra en cada frase
        # 4. Porcentaje de aparicion
        self.count_doc_per_words = self.__create_documents_per_words() #veces que aparece cada palabra en el texto completo
        # 5. Calcular IDF y generar matriz
        self.idf_matrix = self.__create_idf_matrix()
        # 6. Calcular TF*IDF y generar matriz
        self.tf_idf_matrix = self.__create_tf_idf_matrix()
        # 7. Puntuar frases
        self.sentenceValue = self.__score_sentences()
        # 8. Marcar limite
        self.threshold = self.__find_average_score()
        # 9. Generar resumen
        self.summary = self.__generate_summary()
        self.text = self.summary

    def __procesar_texto(self):
        summ = self.text.replace("\n", " ").replace("¿","").replace("?",'.')
        summ = summ.replace("•", "")
        summ = " ".join(summ.split())
        return summ
    
    def __create_frequency_matrix(self):
        frequency_matrix = {}
        stopWords = set(stopwords.words("spanish"))
        ps = PorterStemmer()
        for sent in self.sentences:
            freq_table = {}
            words = word_tokenize(sent)
            for word in words:
                word = word.lower()
                word = ps.stem(word)
                if word in stopWords:
                    continue
                if word in freq_table:
                    freq_table[word] += 1
                else:
                    freq_table[word] = 1
            frequency_matrix[sent[:15]] = freq_table
        return frequency_matrix
    
    def __create_tf_matrix(self):
        tf_matrix = {}
        for sent, f_table in self.freq_matrix.items():
            tf_table = {}
            count_words_in_sentence = len(f_table)
            for word, count in f_table.items():
                tf_table[word] = count / count_words_in_sentence

            tf_matrix[sent] = tf_table
        return tf_matrix
    
    def __create_documents_per_words(self):
        word_per_doc_table = {}
        for sent, f_table in self.freq_matrix.items():
            for word, count in f_table.items():
                if word in word_per_doc_table:
                    word_per_doc_table[word] += 1
                else:
                    word_per_doc_table[word] = 1
        return word_per_doc_table
    
    def __create_idf_matrix(self):
        idf_matrix = {}
        for sent, f_table in self.freq_matrix.items():
            idf_table = {}
            for word in f_table.keys():
                idf_table[word] = math.log10(self.total_documents / float(self.count_doc_per_words[word]))
            idf_matrix[sent] = idf_table
        return idf_matrix

    def __create_tf_idf_matrix(self):
        tf_idf_matrix = {}
        for (sent1, f_table1), (sent2, f_table2) in zip(self.tf_matrix.items(), self.idf_matrix.items()):
            tf_idf_table = {}
            for (word1, value1), (word2, value2) in zip(f_table1.items(), f_table2.items()):  # here, keys are the same in both the table
                tf_idf_table[word1] = float(value1 * value2)
            tf_idf_matrix[sent1] = tf_idf_table
        return tf_idf_matrix

    def __score_sentences(self) -> dict:
        """
        score a sentence by its word's TF
        Basic algorithm: adding the TF frequency of every non-stop word in a sentence divided by total no of words in a sentence.
        :rtype: dict
        """
        sentenceValue = {}
        for sent, f_table in self.tf_idf_matrix.items():
            total_score_per_sentence = 0
            count_words_in_sentence = len(f_table)
            for word, score in f_table.items():
                total_score_per_sentence += score
            sentenceValue[sent] = total_score_per_sentence / count_words_in_sentence
        return sentenceValue
    
    def __find_average_score(self) -> int:
        """
        Find the average score from the sentence value dictionary
        :rtype: int
        """
        sumValues = 0
        for entry in self.sentenceValue:
            sumValues += self.sentenceValue[entry]
        # Average value of a sentence from original summary_text
        average = (sumValues / len(self.sentenceValue))
        return average
    
    def __generate_summary(self):
        sentence_count = 0
        summary = ''
        for sentence in self.sentences:
            if sentence[:15] in self.sentenceValue and self.sentenceValue[sentence[:15]] >= (self.threshold):
                summary += " " + sentence
                sentence_count += 1
        return summary

if __name__ == "__main__":
    # analyzer = TXTanalyzer('tiktok.txt')
    # print(analyzer.sia())
    summarizer = TXTsummarizer('tiktok.txt')
    print(summarizer.sia())