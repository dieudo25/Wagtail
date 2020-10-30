from django.conf import settings
from django.urls import include, re_path
from django.contrib import admin

from wagtail.admin import urls as wagtailadmin_urls
from wagtail.core import urls as wagtail_urls
from wagtail.contrib.sitemaps.views import sitemap
from wagtail.documents import urls as wagtaildocs_urls

from search import views as search_views
from .api import api_router



urlpatterns = [
    re_path('^django-admin/', admin.site.urls),

    re_path('^admin/', include(wagtailadmin_urls)),
    re_path('^documents/', include(wagtaildocs_urls)),

    re_path('^search/$', search_views.search, name='search'),

    re_path('^api/v2/', api_router.urls),

    re_path('^sitemap.xml$', sitemap),

]


if settings.DEBUG:
    from django.conf.urls.static import static
    from django.contrib.staticfiles.urls import staticfiles_urlpatterns

    # Serve static and media files from development server
    urlpatterns += staticfiles_urlpatterns()
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

    import debug_toolbar 

    urlpatterns += [
    re_path('^__debug__/', include(debug_toolbar.urls)),
]

urlpatterns = urlpatterns + [
    # For anything not caught by a more specific rule above, hand over to
    # Wagtail's page serving mechanism. This should be the last pattern in
    # the list:
    re_path("^", include(wagtail_urls)),

    # Alternatively, if you want Wagtail pages to be served from a subpath
    # of your site, rather than the site root:
    #    path("pages/", include(wagtail_urls)),
]
