from django.urls import path

from .views import (
    AddAvatarView,
    AdminToUser,
    AutoParkListCreateView,
    ResetPasswordView,
    SaveNewPasswordView,
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
    path('/auto_parks', AutoParkListCreateView.as_view()),
    path('/avatar', AddAvatarView.as_view()),
    path('/reset_password', ResetPasswordView.as_view()),
    path('/save_password/<str:token>', SaveNewPasswordView.as_view())
]

