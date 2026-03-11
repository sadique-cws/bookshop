
from django.contrib import admin
from django.urls import path
from ecom.views import *
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path("", homepage, name="homepage"),
    path("filter/", filter, name="filter"),
    path("book-view/",book_view, name="book_view")
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
