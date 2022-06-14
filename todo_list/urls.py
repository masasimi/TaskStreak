from django.urls import path

from . import views

handler500 = views.my_customized_server_error
urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.register_view, name='register'),
    path('task/create/', views.create_task, name='create_task'),
    path('task/update/', views.update_task, name='update_task'),
    path('task/delete/', views.delete_task, name='delete_task'),
    path('task/done/', views.done_task, name='done_task'),
    path("task/new/", views.new_form_view, name="form"),
    path("task/edit/", views.edit_form_view, name="form"),
    path("task/detail/", views.detail_view, name="detail"),
]
