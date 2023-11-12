.. TXTanalyzer documentation master file, created by
   sphinx-quickstart on Wed Nov  1 19:18:53 2023.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to TXTanalyzer's documentation!
=======================================

.. toctree::
   :maxdepth: 2
   :caption: Contents:

   modules


Librería TXTanalyzer
=====================================

Introducción
============

TXTanalyzer es una herramienta que permite realizar análisis de texto en archivos .txt. Facilita el análisis de textos a través de diversas herramientas y funcionalidades, como el conteo de palabras, la división de oraciones, el análisis de sentimientos y más. Está basada en librerías populares como spaCy y nltk para mejorar la calidad de los resultados.

TXTanalyzer class
==================

La clase :class:`TXTanalyzer` es la clase principal de la librería y la que hereda en la clase :class:`TXTsummarizer`

.. class:: TXTanalyzer

   :param txt_file_path: La ruta al archivo de texto a analizar.

   Constructor de la clase que lee el contenido de un archivo de texto especificado y lo almacena en el objeto.

   :raises Exception: Se lanza una excepción si el archivo está vacío.

   .. method:: read_file(txt_file_path)

      :param txt_file_path: La ruta al archivo de texto a leer.

      Lee el contenido de un archivo de texto y lo devuelve como una cadena de texto.

      :raises Exception: Se lanza una excepción si el archivo no tiene una extensión .txt.

   .. method:: print_text()

      Devuelve el texto almacenado en el objeto.

   .. method:: sentence_splitting()

      Divide el texto en frases utilizando el modelo de lenguaje "en_core_web_sm" de SpaCy.

   .. method:: word_count()

      Procesa el texto para calcular estadísticas, incluyendo el recuento de palabras, el recuento de palabras únicas y el recuento total de caracteres. Las 'stopwords' son previamente eliminadas.

   .. method:: word_freq()

      Calcula la frecuencia de las palabras en el texto y devuelve un diccionario que asocia cada palabra con su frecuencia.

   .. method:: wordcloud()

      Crea y muestra una representación de nube de palabras basada en la frecuencia de las palabras en el texto.

   .. method:: sia()

      Realiza un análisis de sentimiento (Sentiment Intensity Analyzer - SIA) en el texto y devuelve los resultados.

TXTsummarizer class
==================

La clase :class:`TXTsummarizer` extiende la funcionalidad de :class:`TXTanalyzer` y agrega capacidades de resumen de texto.

.. class:: TXTsummarizer

   :param txt_file_path: La ruta al archivo de texto a procesar y resumir.

   Constructor de la clase que realiza el procesamiento y generación de un resumen a partir de un archivo de texto.

   :raises Exception: Se lanza una excepción si el archivo está vacío.

   .. method:: __procesar_texto()

      Procesa el texto eliminando saltos de línea, signos de interrogación, signos de exclamación y viñetas, y realiza una limpieza adicional eliminando espacios duplicados.

   .. method:: __create_frequency_matrix()

      Crea una matriz de frecuencia que asocia las palabras en las oraciones del texto con su frecuencia de aparición.

   .. method:: __create_tf_matrix()

      Crea una matriz TF (Frecuencia de Términos) que representa la frecuencia relativa de las palabras en las oraciones.

   .. method:: __create_documents_per_words()

      Crea una tabla que asocia las palabras con la cantidad de documentos en los que aparecen.

   .. method:: __create_idf_matrix()

      Crea una matriz IDF (Frecuencia Inversa de Documentos) que representa el valor IDF de cada palabra en el texto.

   .. method:: __create_tf_idf_matrix()

      Crea una matriz TF-IDF que representa el producto de la matriz TF (Frecuencia de Términos) y la matriz IDF (Frecuencia Inversa de Documentos) para cada palabra en el texto.

   .. method:: __score_sentences()

      Evalúa la puntuación de cada oración en función de la TF-IDF de sus palabras.

   .. method:: __find_average_score()

      Calcula el puntaje promedio a partir del diccionario de valores de las oraciones.

   .. method:: __generate_summary()

      Genera un resumen a partir de las oraciones del texto en función de sus puntuaciones.

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
