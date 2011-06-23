from django.conf.urls.defaults import *

urlpatterns = patterns('app.orders.views',
                       #ORDER
                       url(r'^order/$', 'order.overview'),
                       url(r'^order/my$', 'order.my_orders'),
                       url(r'^order/(?P<id>\d+)/view/$', 'order.view'),
                       url(r'^order/new/$', 'order.add'),
                       url(r'^order/(?P<id>\d+)/edit/$', 'order.edit'),
                       url(r'^order/(?P<id>\d+)/statistics/$', 'order.view_statistics'),
                       url(r'^order/(?P<id>\d+)/preview_html/$', 'order.preview_order_html'),
                       url(r'^order/(?P<id>\d+)/invoice/$', 'order.create_invoice'),

                       #Files
                       url(r'^(?P<id>\d+)/files/$', 'files.overview'),
                       url(r'^(?P<id>\d+)/files/add/$', 'files.add_file'),
                       url(r'^(?P<id>\d+)/files/(?P<file_id>\d+)/edit/$', 'files.edit_file'),

                       )