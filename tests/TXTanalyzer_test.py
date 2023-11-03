import sys
sys.path.append("..")
from TXTanalyzer import *

if __name__ == "__main__":
    texto = TXTanalyzer('test_file.txt')
    print(texto.print_text())
    print("#################################")
    print(texto.sentence_splitting())
    print("#################################")
    print(texto.word_count())
    print("#################################")
    print(texto.word_freq())
    print("#################################")
    print(texto.wordcloud())
    print("#################################")
    print(texto.sia())
    print("#################################")
    resumen = TXTsummarizer('test_file.txt')
    print(resumen.print_text())