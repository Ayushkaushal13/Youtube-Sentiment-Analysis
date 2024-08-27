from googleapiclient.discovery import build
from textblob import TextBlob

API_KEY = 'AIzaSyDpmUnTRzV_RwydQAd-TahzSfrCscJCiOo'
YOUTUBE_API_SERVICE_NAME = 'youtube'
YOUTUBE_API_VERSION = 'v3'

def get_youtube_comments(video_id):
    youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION, developerKey=API_KEY)
    comments = []
    results = youtube.commentThreads().list(
        part='snippet',
        videoId=video_id,
        textFormat='plainText'
    ).execute()

    for item in results.get('items', []):
        comment_text = item['snippet']['topLevelComment']['snippet']['textDisplay']
        comments.append(comment_text)
    return comments

def analyze_sentiment(comment_text):
    analysis = TextBlob(comment_text)
    polarity = analysis.sentiment.polarity
    if polarity>0:
     return "positive"
    elif polarity<0:
     return "negative"
    else:
     return "neutral"
