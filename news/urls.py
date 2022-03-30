from django.contrib import admin
from django.urls import path, include
import parse.views as parse_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('parse/', parse_views.parse_news, name='parse'),
    path('', parse_views.index, name="index"),
    path('pages/', parse_views.pages, name="pages"),
    path('analysis/', parse_views.analysis, name="analysis"),
    path('update/', parse_views.update, name="update")
]
