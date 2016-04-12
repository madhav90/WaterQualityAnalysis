from django.shortcuts import render
from django.db import connection
#from models import ExampleModel
from django.http import HttpResponse

def index(request):
    results = ("select * from SampleModel")
    #return HttpResponse(result.p_type)
    return render(request, 'index.html', {'results':results})

def ccme(request):
    db = connection

    # prepare a cursor object using cursor() method
    cursor = db.cursor()

    # execute SQL query using execute() method.
    cursor.execute("SELECT * from trial")

    # Fetch a single row using fetchone() method.
    data = cursor.fetchone()

    print "Database version : %s " % data

    # disconnect from server
    db.close()
    return render(request, 'wqiAnalysis.html',{})