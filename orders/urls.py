from django.urls import path
from . import views
urlpatterns = [
    path("", views.dashboard, name="dashboard"),
    path("clients/add/", views.client_create, name="client_create"),
    path("clients/<int:pk>/edit/", views.client_edit, name="client_edit"),
    path("clients/<int:pk>/delete/", views.client_delete, name="client_delete"),
    path("add/", views.order_create, name="order_create"),
    path("<int:pk>/edit/", views.order_edit, name="order_edit"),
    path("<int:pk>/delete/", views.order_delete, name="order_delete"),
    path("dishes/<int:pk>/photo/", views.dish_photo, name="dish_photo"),
]
