from distutils.core import setup
setup(
  name = 'TXTanalyzer',
  packages = ['TXTanalyzer'],   # Chose the same as "name"
  version = '0.1',      # Start with a small number and increase it with every change you make
  license='GNU',        # Chose a license from here: https://help.github.com/articles/licensing-a-repository
  description = 'The TXTanalyzer library is a tool designed to perform basic text analysis on .txt files. It offers a range of utilities for text analysis, including word counting, sentence splitting, sentiment analysis, and word cloud generation.',   # Give a short description about your library
  author = 'Unai Alaña y Maialen Aguiriano',                   # Type in your name
  author_email = 'unai.alana@alumni.mondragon.edu',      # Type in your E-Mail
  url = 'https://github.com/maialenaguiriano/TXTanalyzer',   # Provide either the link to your github or to your website
  download_url = 'https://github.com/maialenaguiriano/TXTanalyzer/archive/refs/tags/v0.1.tar.gz',    # I explain this later on
  keywords = ['Text', 'Analysis', 'NLP'],   # Keywords that define your package best
  install_requires=[            # I get to this in a second
          'nltk',
          'spacy',
          'string',
          'matplotlib',
          'math',
          'wordcloud'
      ],
  classifiers=[
    'Development Status :: 3 - Alpha',      # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
    'Intended Audience :: Developers',      # Define that your audience are developers
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: GNU Affero General Public License v3',   # Again, pick a license
    'Programming Language :: Python :: 3',    #Specify which pyhton versions that you want to support
    'Programming Language :: Python :: 3.7',
    'Programming Language :: Python :: 3.8',
    'Programming Language :: Python :: 3.9'
  ],
)