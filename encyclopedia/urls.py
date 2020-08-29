from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("search/<str:search>", views.search, name="search"),
    path("wiki/<str:entry>", views.entry, name="entry"),
    path("CreateNewPage", views.Create_New_Page, name="create_new_page"),
    path('edit/<str:page>', views.edit, name='edit'),
    path('randompage', views.random_page, name='random_page')
]
