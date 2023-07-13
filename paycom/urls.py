from django.urls import path

from paycom.views import CardCreateAPIView, CardVerifyAPIView, PaymentApiView

urlpatterns = [
    path('create-card', CardCreateAPIView.as_view(), name='card_create'),
    path('verify-card', CardVerifyAPIView.as_view(), name='card_verify'),
    path('payment', PaymentApiView.as_view(), name='payment'),
]