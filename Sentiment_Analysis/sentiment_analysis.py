import pandas as pd
from nltk.sentiment import SentimentIntensityAnalyzer
import re
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

nltk.download("stopwords")
nltk.download("wordnet")
nltk.download("vader_lexicon")

sia = SentimentIntensityAnalyzer()
stop_words = set(stopwords.words("english"))
lemmatizer = WordNetLemmatizer()

def load_data(file_path):
    df = pd.read_csv(file_path)
    df = df[['Review']]  
    return df

def clean_text(text):
    if isinstance(text, float):  
        return ""
    text = text.lower()  
    text = re.sub(r'[^a-zA-Z0-9\s]', '', text)  
    words = text.split()
    words = [lemmatizer.lemmatize(word) for word in words if word not in stop_words]
    return " ".join(words)

def get_sentiment(text):
    text = clean_text(text)
    vader_score = sia.polarity_scores(text)['compound']
    vader_sentiment = 'Positive' if vader_score > 0.05 else 'Negative' if vader_score < -0.05 else 'Neutral'
    return vader_sentiment, vader_score

def analyze_sentiment(file_path, output_file_path):
    df = load_data(file_path)
    df.drop_duplicates(inplace=True)
    df = df[df['Review'].str.lower() != 'no reviews found']  
    df[['Sentiment', 'Polarity']] = df['Review'].apply(lambda x: pd.Series(get_sentiment(x)))
    df[['Review', 'Sentiment', 'Polarity']].to_csv(output_file_path, index=False)
    print(f"Sentiment analysis results saved to {output_file_path}")

file_path = 'reviews_grubhub.csv'  
output_file_path = 'sentiment_analysis_grubhub.csv'  
analyze_sentiment(file_path, output_file_path)

file_path = 'reviews_ubereats.csv'  
output_file_path = 'sentiment_analysis_ubereats.csv'  
analyze_sentiment(file_path, output_file_path)