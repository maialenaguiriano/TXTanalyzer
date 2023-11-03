import nltk, spacy, spacy.cli, string, matplotlib.pyplot as plt, math
from nltk import sent_tokenize, word_tokenize, PorterStemmer
from nltk.corpus import stopwords
from nltk.sentiment import SentimentIntensityAnalyzer
from wordcloud import WordCloud
from TXTanalyzer import TXTanalyzer

class TXTsummarizer(TXTanalyzer):
    def __init__(self, txt_file_path:str):
        """
        Constructor de la clase. Realiza el procesamiento y generación de un resumen a partir de un archivo de texto.

        Args:
            txt_file_path (str): La ruta al archivo de texto a procesar y resumir.

        Raises:
            Exception: Se lanza una excepción si el archivo está vacío.
        """
        super().__init__(txt_file_path)
        self.text = self.read_file(txt_file_path)
        if self.text == "":
            raise Exception("El fichero no puede estar vacío. Debe contener algún tipo de texto.")
        
        self.summ = self.__procesar_texto()
        # 1. Tokenizar
        self.sentences = sent_tokenize(self.summ)
        self.total_documents = len(self.sentences)
        # 2. Crear matriz de frecuencias
        self.freq_matrix = self.__create_frequency_matrix()
        # 3. Calcular TermFrequency y generar matriz
        self.tf_matrix = self.__create_tf_matrix()
        # 4. Porcentaje de aparicion
        self.count_doc_per_words = self.__create_documents_per_words()
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
        # Guardar resumen en la variable text para aplicar las funciones de TXTanalyzer
        self.text = self.summary

    def __procesar_texto(self):
        """
        Procesa el texto eliminando saltos de línea, signos de interrogación, signos de exclamación y viñetas,
        y realiza una limpieza adicional eliminando espacios duplicados.

        Returns:
            str: El texto procesado.
        """
        summ = self.text.replace("\n", " ").replace("¿","").replace("?",'.')
        summ = summ.replace("•", "")
        summ = " ".join(summ.split())
        return summ
    
    def __create_frequency_matrix(self):
        """
        Crea una matriz de frecuencia que asocia las palabras en las oraciones del texto con su frecuencia de aparición.

        Returns:
            dict: Un diccionario que contiene las frecuencias de las palabras en las oraciones del texto.
        """
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
        """
        Crea una matriz TF (Frecuencia de Términos) que representa la frecuencia relativa de las palabras en las oraciones.

        Returns:
            dict: Un diccionario que contiene la matriz TF del texto.
        """
        tf_matrix = {}
        for sent, f_table in self.freq_matrix.items():
            tf_table = {}
            count_words_in_sentence = len(f_table)
            for word, count in f_table.items():
                tf_table[word] = count / count_words_in_sentence

            tf_matrix[sent] = tf_table
        return tf_matrix
    
    def __create_documents_per_words(self):
        """
        Crea una tabla que asocia las palabras con la cantidad de documentos en los que aparecen.

        Returns:
            dict: Un diccionario que contiene la cantidad de documentos en los que aparece cada palabra.
        """
        word_per_doc_table = {}
        for sent, f_table in self.freq_matrix.items():
            for word, count in f_table.items():
                if word in word_per_doc_table:
                    word_per_doc_table[word] += 1
                else:
                    word_per_doc_table[word] = 1
        return word_per_doc_table
    
    def __create_idf_matrix(self):
        """
        Crea una matriz IDF (Frecuencia Inversa de Documentos) que representa el valor IDF de cada palabra en el texto.

        Returns:
            dict: Un diccionario que contiene la matriz IDF del texto.
        """
        idf_matrix = {}
        for sent, f_table in self.freq_matrix.items():
            idf_table = {}
            for word in f_table.keys():
                idf_table[word] = math.log10(self.total_documents / float(self.count_doc_per_words[word]))
            idf_matrix[sent] = idf_table
        return idf_matrix

    def __create_tf_idf_matrix(self):
        """
        Crea una matriz TF-IDF que representa el producto de la matriz TF (Frecuencia de Términos) y la matriz IDF
        (Frecuencia Inversa de Documentos) para cada palabra en el texto.

        Returns:
            dict: Un diccionario que contiene la matriz TF-IDF del texto.
        """
        tf_idf_matrix = {}
        for (sent1, f_table1), (sent2, f_table2) in zip(self.tf_matrix.items(), self.idf_matrix.items()):
            tf_idf_table = {}
            for (word1, value1), (word2, value2) in zip(f_table1.items(), f_table2.items()):  # here, keys are the same in both the table
                tf_idf_table[word1] = float(value1 * value2)
            tf_idf_matrix[sent1] = tf_idf_table
        return tf_idf_matrix

    def __score_sentences(self):
        """
        Evalúa la puntuación de cada oración en función de la TF-IDF de sus palabras. El algoritmo básico consiste en sumar la frecuencia TF-IDF de cada palabra no vacía en una oración y
        dividirla por el número total de palabras en la oración.

        Returns:
            dict: Un diccionario que asocia cada oración con su puntuación.
        """
        sentenceValue = {}
        for sent, f_table in self.tf_idf_matrix.items():
            total_score_per_sentence = 0
            count_words_in_sentence = len(f_table)
            for word, score in f_table.items():
                total_score_per_sentence += score
            sentenceValue[sent] = total_score_per_sentence / count_words_in_sentence
        return sentenceValue
    
    def __find_average_score(self):
        """
        Calcula el puntaje promedio a partir del diccionario de valores de las oraciones.

        Returns:
            int: El puntaje promedio de las oraciones.
        """
        sumValues = 0
        for entry in self.sentenceValue:
            sumValues += self.sentenceValue[entry]
        # Average value of a sentence from original summary_text
        average = (sumValues / len(self.sentenceValue))
        return average
    
    def __generate_summary(self):
        """
        Genera un resumen a partir de las oraciones del texto en función de sus puntuaciones.

        Returns:
            str: Un resumen generado a partir de las oraciones seleccionadas.
        """
        sentence_count = 0
        summary = ''
        for sentence in self.sentences:
            if sentence[:15] in self.sentenceValue and self.sentenceValue[sentence[:15]] >= (self.threshold):
                summary += " " + sentence
                sentence_count += 1
        return summary
