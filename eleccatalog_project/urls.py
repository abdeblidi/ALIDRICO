"""
URL configuration for eleccatalog_project project.
"""

from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls.i18n import i18n_patterns
from django.contrib import admin
from django.urls import path, include, re_path
from django.views.static import serve


# =========================================================
# Language-independent URLs
# =========================================================

urlpatterns = [

    path(
        'i18n/',
        include('django.conf.urls.i18n')
    ),

    # Django Admin
    path(
        'admin/',
        admin.site.urls
    ),
]


# =========================================================
# Localized URLs
# =========================================================

urlpatterns += i18n_patterns(

    path(
        '',
        include('catalog.urls')
    ),

    path(
        'dashboard/',
        include('dashboard.urls')
    ),

    prefix_default_language=False,
)


# =========================================================
# Development: Media & Static
# =========================================================

urlpatterns += [

    re_path(
        r'^media/(?P<path>.*)$',
        serve,
        {
            'document_root': settings.MEDIA_ROOT
        }
    ),

    re_path(
        r'^static/(?P<path>.*)$',
        serve,
        {
            'document_root': settings.STATIC_ROOT
        }
    ),

]