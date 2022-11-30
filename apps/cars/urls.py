from django.urls import path

from .views import CarsListView, CarRetrieveUpdateDestroyView

urlpatterns = [
    path('', CarsListView.as_view()),
    path('/<int:pk>', CarRetrieveUpdateDestroyView.as_view())
]
