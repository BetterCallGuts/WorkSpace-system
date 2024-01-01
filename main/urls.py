from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from Thoth.admin import final_boss
from django.conf.urls.i18n import i18n_patterns

urlpatterns = [

path("i18n/", include("django.conf.urls.i18n")),
path('', include("Thoth.urls")),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
# print("*"*200)
# print(static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT))
final_boss.site_title = "Thuth"
final_boss.site_header = "Thuth"
final_boss.index_title = "Dash Board"



urlpatterns += i18n_patterns(path("Caffe/", final_boss.urls))