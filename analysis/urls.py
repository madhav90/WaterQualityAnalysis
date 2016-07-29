from django.conf.urls import url
from . import views

urlpatterns = [ url(r'^$', views.index, name='index'),
                url(r'^analysis', views.cluster, name='cluster'),
                # url(r'^spider', views.spider, name='spider'),
                # url(r'^ajaxChange', views.spiderAjax, name='spiderchange'),
                url(r'^qualityTrends', views.qualityTrends, name='qT'),
                url(r'^getSensorData', views.getSensorData, name='sensorData'),
                url(r'^kmeans', views.kmeans, name='kmeans'),
               ]
