from django.urls import path
from .           import views
from rest_framework.urlpatterns import format_suffix_patterns
# from .admin import admin_site

urlpatterns = [
path('', views.admin),
path('getrecpdata/', views.get_resp_data, name='get_resp_data'),
path("getalldata/", views.get_all_data, name="get_all_data"),
path("addrecpdata", views.add_resp_data,name='addrecpdata'),
# path("**", views.wrong_page)
]

urlpatterns = format_suffix_patterns(urlpatterns, allowed=['json'])