# TXTanalyzer

TXTanalyzer is a Python library designed for basic text analysis of .txt files. It provides a variety of text analysis utilities, including word counting, sentence splitting, sentiment analysis, and word cloud generation. The library is built using popular Python libraries such as spaCy, NLTK, and WordCloud to enhance the quality of text analysis.

## Table of Contents
1. [Installation](#installation)
2. [Getting Started](#getting-started)
3. [Utilities](#utilities)
4. [Examples](#examples)
5. [Contributing](#contributing)

## Installation <a name="installation"></a>

To use the TXTanalyzer library, you need to install the required Python packages. You can install these packages using pip:

```bash
pip install spacy nltk matplotlib wordcloud
```

After installing the necessary packages, you must install the library and import it into your Python script. The library consists of two main modules: TXTanalyzer and TXTsummarizer.

```bash
# Install the library from PyPI
pip install TXTanalyzer
pip install TXTanalyzer==1.2

# Import the modules
from TXTanalyzer import TXTanalyzer, TXTsummarizer
```

## Getting Started <a name="getting-started"></a>

The TXTanalyzer library provides a range of functionalities for text analysis. You can use it to analyze text from .txt files and perform various tasks. Here's a quick overview of the key functionalities:

### TXTanalyzer

The `TXTanalyzer` class is designed to analyze and provide insights on text from .txt files. It includes the following functions:

- `read_file(txt_file_path)`: Reads the content of a specified .txt file.
- `print_text()`: Retrieves the stored text from the object.
- `sentence_splitting()`: Splits the text into sentences using SpaCy's "en_core_web_sm" language model.
- `word_count()`: Calculates word count, unique word count, and total character count, after removing stopwords and punctuation.
- `word_freq()`: Calculates word frequency in the text.
- `wordcloud()`: Generates and displays a word cloud based on word frequency.
- `sia()`: Performs sentiment analysis using Sentiment Intensity Analyzer (SIA) and provides negativity, neutrality, and positivity scores.

### TXTsummarizer

The `TXTsummarizer` class, which inherits from `TXTanalyzer`, provides text summarization capabilities. It includes the following functions:

- `__procesar_texto()`: Processes the text, removing line breaks, question marks, exclamation marks, and bullets.
- `__create_frequency_matrix()`: Creates a frequency matrix associating words with their frequency in sentences.
- `__create_tf_matrix()`: Creates a TF (Term Frequency) matrix representing the relative frequency of words in sentences.
- `__create_documents_per_words()`: Creates a table that associates words with the number of documents they appear in.
- `__create_idf_matrix()`: Creates an IDF (Inverse Document Frequency) matrix representing the IDF value of each word in the text.
- `__create_tf_idf_matrix()`: Creates a TF-IDF matrix for each word in the text.
- `__score_sentences()`: Evaluates sentence scores based on the TF-IDF of their words.
- `__find_average_score()`: Calculates the average sentence score.
- `__generate_summary()`: Generates a summary based on selected sentences with scores above a certain threshold.

To get started, create an instance of `TXTsummarizer` by providing the path to a .txt file and use its summarization capabilities.

## Utilities <a name="utilities"></a>

The library uses various Python libraries, including spaCy, NLTK, and WordCloud, to enhance text analysis. Make sure to install these libraries as described in the installation section.

## Examples <a name="examples"></a>

Here are some code examples on how to use the TXTanalyzer library:

```python
# Import the necessary modules
from TXTanalyzer import TXTanalyzer, TXTsummarizer

# Create an instance of TXTanalyzer with a .txt file
analyzer = TXTanalyzer("example.txt")

# Perform text analysis using TXTanalyzer's functions
text = analyzer.print_text()
sentences = analyzer.sentence_splitting()
statistics = analyzer.word_count()
word_frequencies = analyzer.word_freq()
analyzer.wordcloud()
sentiment_analysis = analyzer.sia()

# Create an instance of TXTsummarizer for text summarization
summarizer = TXTsummarizer("example.txt")

# Get the generated summary
summary = summarizer.text

# Perform additional analysis on the generated summary using TXTanalyzer's functions
summary_sentences = summarizer.sentence_splitting()
summary_statistics = summarizer.word_count()
summary_word_frequencies = summarizer.word_freq()
summarizer.wordcloud()
summary_sentiment_analysis = summarizer.sia()
```

## Contributing <a name="contributing"></a>

If you would like to contribute to the development of the TXTanalyzer library or report issues, please visit the GitHub repository [here](https://github.com/your-repo).

Enjoy analyzing and summarizing your text with TXTanalyzer!