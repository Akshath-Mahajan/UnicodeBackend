from django.urls import path
from .views import Home, ListDetails, ToggleComplete,Timeline, TaskCreate, TaskDelete, ListCreate, ListUpdate, ListDelete
urlpatterns = [
    path('', Home.as_view(), name="home"),
    path('list/create', ListCreate.as_view(), name="list_create"),
    path('list/<int:pk>/', ListDetails.as_view(), name="list_details"),
    path('list/<int:pk>/update', ListUpdate.as_view(), name="list_update"),
    path('list/<int:pk>/delete', ListDelete.as_view(), name="list_delete"),
    path('list/<int:pk>/create-task', TaskCreate.as_view(), name="task_create"),
    path('task/toggle-complete/', ToggleComplete.as_view(), name="toggle_complete"),
    path('task/delete/<int:pk>', TaskDelete.as_view(), name="task_delete"),
    path('timeline', Timeline.as_view(), name="timeline"),
]
