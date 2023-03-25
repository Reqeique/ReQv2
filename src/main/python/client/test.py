
import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer

nltk.download('vader_lexicon')
nltk.download('averaged_perceptron_tagger')
sia = SentimentIntensityAnalyzer()

def analyze_sentiment(user_input):
    tokens = nltk.word_tokenize(user_input)
    tagged = nltk.pos_tag(tokens)

    subject = None
    for word, tag in tagged:
        if tag == 'PRP' and word.lower() == 'you':
            subject = word
            break

    if subject:
        score = sia.polarity_scores(user_input)
        return score['compound'] < -0.05
         
    
    #if cpd < -0.05 returns neg


user_input = input("Please enter your message: ")
result = analyze_sentiment(user_input)
print(result)