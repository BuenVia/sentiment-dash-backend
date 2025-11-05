from django.urls import path
from .views import FeedbackListCreate, FeedbackListCreateAI, FeedbackStats, FeedbackSentimentDateRange

urlpatterns = [
    path("feedback/", FeedbackListCreate.as_view(), name="feedback-list-create"),
    path("feedback-ai/", FeedbackListCreateAI.as_view(), name="feedback-list-create-ai"),
    path("feedback-date/", FeedbackSentimentDateRange.as_view(), name="feedback-date"),
    path("stats/", FeedbackStats.as_view(), name="feedback-stats")
]