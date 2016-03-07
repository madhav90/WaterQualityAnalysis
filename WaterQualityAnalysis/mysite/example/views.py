from cassandra.cqlengine import connection
from cassandra.cqlengine.management import sync_table
from cassandra.cluster import Cluster
#from models import ExampleModel
from django.http import HttpResponse

def index(request):
    cluster = Cluster(['127.0.0.1'])
    session = cluster.connect()
    session.set_keyspace('db2')
    #insert = ExampleModel(description="hello")
    #insert.save()
    result = session.execute("select * from SampleModel")[0]
    #print(result.description)
    cluster.shutdown()
    return HttpResponse(result.p_type)
