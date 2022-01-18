from django.urls import path

from authentication.views import TokenLoginView, TestView

app_name = "auth"

urlpatterns = [
    path('login/', TokenLoginView.as_view(), name='login'),
    path('test/', TestView.as_view(), name='login'),
]
