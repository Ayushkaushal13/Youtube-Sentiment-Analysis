from django.shortcuts import render
from django import forms
from .utils import get_youtube_comments, analyze_sentiment
from urllib.parse import urlparse, parse_qs

class YouTubeURLForm(forms.Form):
    video_url = forms.URLField(label='YouTube Video URL', required=True)

def analyze_comments(request):
    if request.method == 'POST':
        form = YouTubeURLForm(request.POST)
        if form.is_valid():
            video_url = form.cleaned_data['video_url']
            video_id = extract_video_id(video_url)
            if not video_id:
                return render(request, 'myapp/submit.html', {
                    'form': form, 
                    'error': 'Invalid YouTube URL'
                })

            comments = get_youtube_comments(video_id)
            sentiments = [analyze_sentiment(comment) for comment in comments]

            # Count the sentiments to determine the majority sentiment
            sentiment_counts = {'positive': 0, 'negative': 0, 'neutral': 0}
            for sentiment in sentiments:
                sentiment_counts[sentiment] += 1

            # Determine the overall sentiment based on counts
            if sentiments:
                if sentiment_counts['positive'] >= sentiment_counts['negative'] and sentiment_counts['positive'] >= sentiment_counts['neutral']:
                    average_sentiment = 'positive'
                elif sentiment_counts['negative'] > sentiment_counts['positive'] and sentiment_counts['negative'] >= sentiment_counts['neutral']:
                    average_sentiment = 'negative'
                else:
                    average_sentiment = 'neutral'
            else:
                average_sentiment = 'neutral'  # Handle cases with no comments

            sentiment_analysis = [
                {'comment': comment, 'sentiment': sentiment}
                for comment, sentiment in zip(comments, sentiments)
            ]

            return render(request, 'myapp/results.html', {
                'sentiments': sentiment_analysis,
                'average_sentiment': average_sentiment,
            })
    else:
        form = YouTubeURLForm()

    return render(request, 'myapp/submit.html', {'form': form})

def extract_video_id(url):
    parsed_url = urlparse(url)
    if parsed_url.hostname in ['www.youtube.com', 'youtube.com']:
        video_id = parse_qs(parsed_url.query).get('v')
        if video_id:
            return video_id[0]
    elif parsed_url.hostname == 'youtu.be':
        return parsed_url.path[1:]  # Remove leading '/'
    return None
