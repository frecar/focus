from django.conf.urls.defaults import *

urlpatterns = patterns('app.admin.views',

                       #User
                       url(r'^users/$', 'user.overview'),
                       url(r'^user/add/$', 'user.add'),
                       url(r'^user/(?P<id>\d+)/edit/$', 'user.edit'),
                       url(r'^user/(?P<id>\d+)/view/$', 'user.view'),
                       url(r'^user/(?P<id>\d+)/permissions/$', 'user.permissions'),
                       url(r'^user/(?P<id>\d+)/delete_permission/(?P<permission_id>\d+)$', 'user.delete_permission'),
                       url(r'^user/(?P<id>\d+)/trash/$', 'user.trash'),
                       url(r'^user/(?P<id>\d+)/history/$', 'user.history'),
                       url(r'^user/(?P<id>\d+)/change_can_login/$', 'user.changeCanLogin'),
                       url(r'^user/(?P<id>\d+)/send_new_password/', 'user.send_generated_password_to_user'),
                       url(r'^user/(?P<id>\d+)/set_time/$', 'user.set_hourregistration_limits'),

                       #Group
                       url(r'^groups/$', 'group.overview'),
                       url(r'^groups/add/$', 'group.add'),
                       url(r'^group/(?P<id>\d+)/edit/$', 'group.edit'),
                       url(r'^group/(?P<id>\d+)/members/$', 'group.members'),
                       url(r'^group/(?P<group_id>\d+)/remove_user/(?P<user_id>\d+)$', 'group.remove_user_from_group'),
                       url(r'^group/(?P<id>\d+)/permissions/$', 'group.permissions'),
                       url(r'^group/(?P<id>\d+)/delete_permission/(?P<permission_id>\d+)$', 'group.delete_permission'),
                       url(r'^group/(?P<id>\d+)/view/$', 'group.view'),
                       url(r'^group/(?P<id>\d+)/delete/$', 'group.delete'),

                       #Profle
                       url(r'^profile/edit/$', 'profile.edit'),
                       url(r'^profile/password/$', 'profile.change_password'),
                       url(r'^profile/image/$', 'profile.change_profile_image'),

                       #Log
                       url(r'^logs/$', 'log.overview'),
                       )