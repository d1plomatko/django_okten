from django.urls import path

from .views import AddCarPhotoView, CarRetrieveUpdateDestroyView, CarsListView

urlpatterns = [
    path('', CarsListView.as_view()),
    path('/<int:pk>', CarRetrieveUpdateDestroyView.as_view()),
    path('/<int:pk>/photo', AddCarPhotoView.as_view())
]
