# -*- coding: utf-8 -*-
from django.conf.urls.defaults import *
from django.conf import settings
import os

urlpatterns = patterns('',
    (r'^$', include('app.dashboard.urls')),
    (r'^dashboard/', include('app.dashboard.urls')),
    (r'^customers/', include('app.customers.urls')),
    (r'^contacts/', include('app.contacts.urls')),
    (r'^company/', include('app.company.urls')),
    (r'^tickets/', include('app.tickets.urls')),
    (r'^projects/', include('app.projects.urls')),
    (r'^accounts/', include('app.accounts.urls')),
    (r'^files/', include('app.files.urls')),

    (r'^orders/', include('app.orders.urls')),
    (r'^offers/', include('app.offers.urls')),
    (r'^invoices/', include('app.invoices.urls')),

    (r'^search/', include('app.search.urls')),
    (r'^hourregistrations/', include('app.hourregistrations.urls')),
    (r'^announcements/', include('app.announcements.urls')),
    (r'^calendar/', include('app.calendar.urls')),

    (r'^email/', include('app.email.urls')),

                       #settings for admin
    (r'^admin/', include('app.admin.urls')),

                       #Stock
    (r'^stock/', include('app.stock.urls')),

                       #API
    (r'^api/', include('api.urls')),

                       #client ticket site
    (r'^client/', include('app.client.urls')),

                       #Suppliers
    (r'^suppliers/', include('app.suppliers.urls')),
    (r'^tickets/', include('app.tickets.urls')),

                       #Grant permissions
    (r'grant/role/(?P<role>\w+)/(?P<userorgroup>\w+)/(?P<user_id>\w+)/(?P<app>\w+)/(?P<model>\w+)/(?P<object_id>\w+)/$'
     , 'core.views.grant_role'),

    (
        r'grant/permission/(?P<perm>\w+)/(?P<userorgroup>\w+)/(?P<user_id>\w+)/(?P<app>\w+)/(?P<model>\w+)/(?P<object_id>\w+)/$'
        , 'core.views.grant_permission'),

    (r'get_postal_by_zip//$', 'core.views.view_postal_by_zip'),
    (r'get_postal_by_zip/(?P<zip>\d+)/$', 'core.views.view_postal_by_zip'),

    (r'^file/(?P<filename>.*)$', 'core.views.retrieve_file'),

    (r'^i18n/', include('django.conf.urls.i18n')),

                       )

if settings.DEBUG:
    from django.contrib.staticfiles.urls import staticfiles_urlpatterns

    urlpatterns += staticfiles_urlpatterns()