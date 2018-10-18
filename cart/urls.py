from django.urls import path

from cart import views



urlpatterns = [
    path('show_cart/', views.Show_cart.as_view(), name='show_cart'),
]



