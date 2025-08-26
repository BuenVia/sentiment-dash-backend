from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from feedback.models import Feedback

class FeedbackAPITests(APITestCase):
    def setUp(self):
        self.url = reverse("feedback-list-create")

    def test_create_feedback(self):
        """Should create feedback and auto-assign sentiment"""
        payload = {
            "name": "John Doe",
            "email": "john@example.com",
            "feedback_text": "The service was fantastic!"
        }
        response = self.client.post(self.url, payload, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn("sentiment_score", response.data)
        self.assertIn("sentiment_label", response.data)
        self.assertEqual(response.data["sentiment_label"], "Positive")

        # Check DB object
        self.assertEqual(Feedback.objects.count(), 1)

    def test_get_feedback_list(self):
        """Should return all submitted feedback"""
        Feedback.objects.create(
            name="Jane",
            email="jane@example.com",
            feedback_text="Not great, could be better",
            sentiment_score=-0.5,
            sentiment_label="Negative"
        )
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["sentiment_label"], "Negative")
