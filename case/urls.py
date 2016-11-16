from django.conf.urls import url
from . import views

app_name = 'case'

urlpatterns = [
    url(r'^$', views.index, name='index'),

    url(r'^register/$', views.register, name='register'),
    url(r'^login_user/$', views.login_user, name='login_user'),
    url(r'^logout_user/$', views.logout_user, name='logout_user'),

    url(r'^(?P<case_id>[0-9]+)/$', views.detail, name='detail'),
    url(r'^(?P<case_id>[0-9]+)/json$', views.detail_json, name='detail_json'),
    url(r'^(?P<case_id>[0-9]+)/json/1$', views.detail_json_1, name='detail_json_1'),

    url(r'^coordinates/(?P<filter_by>[a-zA_Z]+)/$', views.coordinates, name='coordinates'), # if filter_by = all => show all coordinates
    url(r'^create_case/$', views.create_case, name='create_case'),
    url(r'^(?P<case_id>[0-9]+)/create_coordinate/$', views.create_coordinate, name='create_coordinate'),
    url(r'^(?P<case_id>[0-9]+)/delete_case/$', views.delete_case, name='delete_case'),
    # url(r'^(?P<case_id>[0-9]+)/favorite_case/$', views.favorite_case, name='favorite_case'),
    # url(r'^(?P<coordinate_id>[0-9]+)/favorite/$', views.favorite, name='favorite'),
    # url(r'^(?P<case_id>[0-9]+)/delete_coordinate/(?P<coordinate_id>[0-9]+)/$', views.delete_coordinate, name='delete_coordinate'),
]
