from django.urls import path
from products import views


urlpatterns = [
    path('', views.index, name='index'),
    path('store/', views.StoreListView.as_view(), name='store'),
    path('product/<int:pk>', views.ProductDetailView.as_view(), name='product-detail'),
    path('addToCart', views.addToCart, name='addItem'),
    path('removeFromCart', views.removeFromCart, name='removeItem'),
    path('order', views.placeOrder, name='beginCheckOut'),
    path('completeOrder', views.completeOrder, name="completeOrder"),
    path('addPaymentCard', views.addPaymentCard, name="addPaymentCard"),
    path("cardForm", views.cardForm, name="cardForm"),
]