from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("<int:listing_id>",views.listing, name="listing"),
    path("categories/<str:category_name>/",views.category, name = "category"),
    path("create/",views.create, name="create"),
    path("categories/",views.categories, name="categories"),
]
