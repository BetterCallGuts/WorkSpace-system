from django.urls import path
from .           import views
from .admin import final_boss
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = [
    path("", views.redirectadmin),
    path("Caffe/", final_boss.urls),
    path('attend/<int:pk>',views.attender, name="attend")
]

