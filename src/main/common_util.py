from nltk.stem import PorterStemmer
from nltk.tokenize import word_tokenize
def stemmer(sent):
   ps = PorterStemmer()
   
  
   words = word_tokenize(sent)
   
   stemmed_words = [ps.stem(word) for word in words]
   return (stemmed_words)

def t2e():
   pass