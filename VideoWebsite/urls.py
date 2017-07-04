"""VideoWebsite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from .views import *
from django.conf.urls.static import static
from django.conf import settings


urlpatterns = [
    # page request
    url(r'^$', homepage),
    url(r'^admin/', admin.site.urls),
    url(r'^uploadpage$', uploadpage),
    url(r'^videos/(?P<part_id>[A-F0-9]{16})/$', video),
    url(r'^deletepage$', deletepage),

    # post request
    url(r'^download', file_download),
    url(r'^video_upload$', video_upload),
    url(r'^delete_video$', video_delete),
    # url(r'^test$', test),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
