from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from Thoth.admin import final_boss

urlpatterns = [
  
path('', include("Thoth.urls")),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
# print("*"*200)
# print(static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT))
final_boss.site_title = "Thuth"
final_boss.site_header = "Thuth"
final_boss.index_title = "Dash Board"
