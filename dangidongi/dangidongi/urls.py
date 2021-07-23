import re

from django.contrib import admin
from django.urls import re_path, path
from django.conf import settings
from django.views.static import serve
from rest_framework.routers import DefaultRouter

from dangidongi import views

urlpatterns = [
    path(
        'admin/',
         admin.site.urls
    ),
    path(
        'api/profile/login/',
        views.LoginAPIView.as_view()
    ),
]

router = DefaultRouter()
router.register(
    'api/profile',
    views.ProfileViewSet
)
router.register(
    'api/group',
    views.GroupViewSet
)

urlpatterns += router.urls

urlpatterns += [
    re_path(
        r'^%s(?P<path>.*)$' % re.escape(settings.STATIC_URL.lstrip('/')),
        serve,
        {'document_root': settings.STATIC_ROOT}
    ),
    re_path(
        r'^%s(?P<path>.*)$' % re.escape(settings.MEDIA_URL.lstrip('/')),
        serve,
        {'document_root': settings.MEDIA_ROOT}
    ),
]
