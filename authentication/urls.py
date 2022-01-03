from django.urls import path

from authentication.views import TokenLoginView

app_name = "auth"

urlpatterns = [
    path('login/', TokenLoginView.as_view(), name='login'),
]
