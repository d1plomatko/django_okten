from django.urls import path

from .views import (
    AdminToUser,
    AutoParkListCreateView,
    UserActivateView,
    UserCreateView,
    UserDeActivateView,
    UserToAdmin,
)

urlpatterns = [
    path('', UserCreateView.as_view()),
    path('/<int:pk>/activate', UserActivateView.as_view()),
    path('/<int:pk>/deactivate', UserDeActivateView.as_view()),
    path('/<int:pk>/to_admin', UserToAdmin.as_view()),
    path('/<int:pk>/to_user', AdminToUser.as_view()),
    path('/auto_parks', AutoParkListCreateView.as_view())
]
