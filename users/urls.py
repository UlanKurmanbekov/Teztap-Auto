from django.urls import path

from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from users.views import UserViewSet, SignUpView, PasswordResetRequestView, PasswordResetConfirmView


urlpatterns = [
    path('<int:pk>/', UserViewSet.as_view({'get': 'retrieve', 'patch': 'partial_update'})),
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('login/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('signup/', SignUpView.as_view(), name='auth_register'),
    path('password-reset/', PasswordResetRequestView.as_view(), name='password-reset-request'),
    path('password-reset-confirm/<str:uidb64>/<str:token>/', PasswordResetConfirmView.as_view(), name='password-reset-confirm'),
]
