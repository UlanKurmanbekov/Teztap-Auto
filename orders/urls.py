from django.urls import path
from orders.views import OrderView


urlpatterns = [
    path('orders/', OrderView.as_view({'get': 'list', 'post': 'create'})),
    path('orders/<int:pk>/', OrderView.as_view({'get': 'retrieve', 'patch': 'partial_update'})),
]
