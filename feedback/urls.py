from django.urls import path
from .views import FeedbackListCreate, FeedbackStats

urlpatterns = [
    path("feedback/", FeedbackListCreate.as_view(), name="feedback-list-create"),
    path("stats/", FeedbackStats.as_view(), name="feedback-stats")
]