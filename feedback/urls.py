from django.urls import path
from .views import FeedbackListCreate, FeedbackStats, FeedbackSentimentDateRange

urlpatterns = [
    path("feedback/", FeedbackListCreate.as_view(), name="feedback-list-create"),
    path("feedback-date/", FeedbackSentimentDateRange.as_view(), name="feedback-date"),
    path("stats/", FeedbackStats.as_view(), name="feedback-stats")
]