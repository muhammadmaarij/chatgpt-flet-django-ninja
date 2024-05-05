# chatbot_project/urls.py

from django.contrib import admin
from django.urls import path
from ninja import NinjaAPI
from chatbot.views import router as chatbot_router

api = NinjaAPI()
api.add_router("/", chatbot_router)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', api.urls),
]
