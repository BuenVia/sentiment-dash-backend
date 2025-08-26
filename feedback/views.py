from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Count
from django.db.models.functions import TruncDate
from .models import Feedback
from .serilaizers import FeedbackSerializer
from .sentiment import analyze_sentiment

class FeedbackListCreate(APIView):
    def get(self, request):
        feedback = Feedback.objects.order_by("-created_at")
        serializer = FeedbackSerializer(feedback, many=True)
        return Response(serializer.data)
    
    def post(self, request):
        serializer = FeedbackSerializer(data=request.data)
        if serializer.is_valid():
            score, label = analyze_sentiment(serializer.validated_data["feedback_text"])
            feedback = Feedback.objects.create(
                name = serializer.validated_data.get("name"),
                email = serializer.validated_data.get("email"),
                feedback_text = serializer.validated_data["feedback_text"],
                sentiment_score=score,
                sentiment_label = label
            )
            return Response(FeedbackSerializer(feedback).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class FeedbackStats(APIView):
    def get(self, request):
        total = Feedback.objects.count()
        distribution = Feedback.objects.values("sentiment_label").annotate(count=Count("id"))
        trend = (
            Feedback.objects.annotate(date=TruncDate("created_at"))
            .values("date", "sentiment_label").annotate(count=Count("id"))
            .order_by("date")
        )
        return Response({
            "total_feedback": total,
            "sentiment_distribution": distribution,
            "trend_over_time": trend
        })