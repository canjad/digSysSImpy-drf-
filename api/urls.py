
from rest_framework import  routers
from api.views import  accout
from django.urls import path

router =routers.SimpleRouter()


# /api/resister
router.register(r'register',accout.registerView,'register')



urlpatterns = [
    path("auth/",accout.AuthView.as_view())
]
