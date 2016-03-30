from cassandra.cqlengine import connection
from cassandra.cqlengine.management import sync_table
from django.shortcuts import render
from cassandra.cluster import Cluster
#from models import ExampleModel
from django.http import HttpResponse

def index(request):
    cluster = Cluster(['127.0.0.1'])
    session = cluster.connect()
    session.set_keyspace('db2')
    #insert = ExampleModel(description="hello")
    #insert.save()
    results = session.execute("select * from SampleModel")[0]
    #print(result.description)
    cluster.shutdown()
    #return HttpResponse(result.p_type)
    return render(request, 'analysis/index.html', {'results':results})

import csv
import urllib2

def collectDataSensor(request):
    req = urllib2.Request('http://pdx.axiomalaska.com/stationsensorservice/getExcelSheet?stationid=20364&sensorid=41&version=2&units=89;microg.L-1&start_time=1384477860&end_time=1458936300')
    response = urllib2.urlopen(req)
    cr = csv.reader(response)
    for row in cr:
        print row


