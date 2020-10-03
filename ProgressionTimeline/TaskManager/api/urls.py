from django.urls import path
from .views import ListDetail, TaskDetail, TaskUpdate, TaskDelete, TaskCreate, ListCreate, ListUpdate, ListDelete
from rest_framework.authtoken.views import obtain_auth_token
urlpatterns = [
    path('task/<int:pk>', TaskDetail),
    path('task/create', TaskCreate.as_view()),
    path('task/<int:pk>/update', TaskUpdate.as_view()),
    path('task/<int:pk>/delete', TaskDelete.as_view()),
    path('list/<int:pk>', ListDetail),
    path('list/create', ListCreate.as_view()),
    path('list/<int:pk>/update', ListUpdate.as_view()),
    path('list/<int:pk>/delete', ListDelete.as_view()),
]