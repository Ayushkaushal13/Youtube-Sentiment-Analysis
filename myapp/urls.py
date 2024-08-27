from django.urls import path
from .views import analyze_comments

urlpatterns = [
    path('analyze-comments/', analyze_comments, name='analyze_comments'),
]
