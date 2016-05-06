from django.conf.urls import url
from . import views

urlpatterns = [ url(r'^$', views.index, name='index'),
                url(r'^analysis', views.ccme, name='ccme'),
                url(r'^cluster', views.cluster, name='cluster'),
                url(r'^qualityTrends', views.qualityTrends, name='qT'),]