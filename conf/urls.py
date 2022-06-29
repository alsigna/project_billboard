"""conf URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.contrib import admin
from django.urls import include, path
from django.conf.urls.static import static
from ckeditor_uploader.views import upload as ckeditor_upload
from ckeditor_uploader.views import browse as ckeditor_browse
from django.views.decorators.cache import never_cache

urlpatterns = [
    path("admin/", admin.site.urls),
    path("accounts/", include("allauth.urls")),
    # path("tinymce/", include("tinymce.urls")),
    # path("ckeditor/", include("ckeditor_uploader.urls")),
    path("", include("board.urls")),
]

urlpatterns += [
    path(r"ckeditor/upload/", ckeditor_upload, name="ckeditor_upload"),
    path(r"ckeditor/browse/", never_cache(ckeditor_browse), name="ckeditor_browse"),
]

if settings.DEBUG:
    urlpatterns += [path("__debug__/", include("debug_toolbar.urls"))]
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
