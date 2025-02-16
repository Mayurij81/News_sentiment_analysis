import requests
import pandas as pd
from textblob import TextBlob
import matplotlib.pyplot as plt
import nltk

# Ensure punkt is downloaded for TextBlob
nltk.download('punkt')

# News API key and URL
API_KEY = '7e739a11a3f942fab736fe86c970dafd'  # News API key
NEWS_URL = 'https://newsapi.org/v2/top-headlines'

# Parameters for API request
params = {
    'country': 'us',   # You can change this to your preferred country code
    'category': 'general',
    'apiKey': API_KEY
}

# Fetching live news
response = requests.get(NEWS_URL, params=params)
news_data = response.json()

# Checking if request was successful
if news_data['status'] == 'ok':
    # Creating DataFrame
    articles = news_data['articles']
    df = pd.DataFrame(articles)
    
    # Display first 5 headlines
    print("Top 5 Headlines:")
    print(df['title'].head())
    
    # Function to calculate sentiment
    def get_sentiment(text):
        analysis = TextBlob(text)
        if analysis.sentiment.polarity > 0:
            return 'Positive'
        elif analysis.sentiment.polarity < 0:
            return 'Negative'
        else:
            return 'Neutral'

    # Applying sentiment analysis to headlines
    df['Sentiment'] = df['title'].apply(lambda x: get_sentiment(x if x else ''))

    # Displaying sentiment counts
    sentiment_counts = df['Sentiment'].value_counts()
    print("\nSentiment Counts:")
    print(sentiment_counts)
    
    # Visualizing sentiment distribution
    plt.figure(figsize=(8, 6))
    sentiment_counts.plot(kind='bar', color='skyblue')
    plt.title('Sentiment Analysis of Live News Headlines')
    plt.xlabel('Sentiment')
    plt.ylabel('Number of Headlines')
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.show()
else:
    print("Failed to retrieve news. Check your API key and network connection.")
