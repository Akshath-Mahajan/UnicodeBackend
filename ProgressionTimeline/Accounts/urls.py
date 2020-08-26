from django.urls import path
from .views import Login, Signup, Profile, Logout
urlpatterns = [
    path('login/', Login.as_view(), name="login"),
    path('signup/', Signup.as_view(), name="signup"),
    path('profile/', Profile.as_view(), name="profile"),
    path('logout/', Logout.as_view(), name="logout"),
]
