from django.urls import path, include
from . import views

app_name = 'api_events'

urlpatterns = [
    path('reviews/create/', views.create_review, name='create_review')
]
