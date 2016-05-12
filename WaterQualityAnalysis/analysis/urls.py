from django.conf.urls import url
from . import views

urlpatterns = [ url(r'^$', views.index, name='index'),
                url(r'^analysis', views.cluster, name='cluster'),
                url(r'^spider', views.spider, name='spider'),
                url(r'^qualityTrends', views.qualityTrends, name='qT'),
                url(r'^getSensorData', views.getSensorData, name='sensorData'),
                url(r'^do_index.html', views.do_index, name='spider'),
                url(r'^ph_index.html', views.ph_index, name='spider'),
                url(r'^salinity_index.html', views.salinity_index, name='spider'),
                url(r'^turbidity_index.html', views.turbidity_index, name='spider'),
                url(r'^watertemp_index.html', views.water_index, name='spider'),
                url(r'^chl_index.html', views.spider, name='spider'),
               ]
