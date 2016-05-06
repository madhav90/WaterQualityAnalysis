from django.shortcuts import render
from django.db import connection
import math
import json
import os.path
from collections import defaultdict
from django.http import HttpResponse


def index(request):
    return render(request, 'index.html', {})

def cluster(request):
    qualitydata = calculateCCMEwqi()
    return render(request, 'cluster.html',{'yearData': json.dumps(qualitydata)})

def ccme(request):
    qualitydata = calculateCCMEwqi()
    return render(request, 'ccmeAnalysis.html',{'data': json.dumps(qualitydata)})

def qualityTrends(request):
    return render(request, 'madhav/index.html',{})

def calculateCCMEwqi():
    db = connection
    cursor = db.cursor()
    cursor.execute("SELECT distinct(station) from usgsdata")
    data = cursor.fetchall()
    ccmedata=[];
    for row in data:
        cursor.execute("select * from usgsdata group by station having station=" + row[0])
        data1 = cursor.fetchone()
        cursor.execute("select latitude,longitude from usgs_station where station=" + row[0])
        coordinate = cursor.fetchone()
        if(coordinate == None):
            continue
        lat = coordinate[0]
        long = coordinate[1]
        numOfVar = 0
        for i in range(2,10):
            if data1[i] != None:
                numOfVar += 1
        cursor.execute("select distinct year(date) from usgsdata where station=" + row[0])
        data2 = cursor.fetchall();
        for row2 in data2:
            k= str(row2[0])
            cursor.execute("select * from usgsdata where station=" + row[0] + " and year(date)=" + k)
            data3=cursor.fetchall();
            outOfRangeValue = 0;
            totalValue=0;
            totalExcursion=0;
            dict={};
            for row3 in data3:
                for j in range(2,10):
                    if row3[j] != None:
                        totalValue += 1
                        flag,excursion = checkRange(row3[j],j)
                        totalExcursion += excursion
                        if flag == 1:
                            outOfRangeValue +=1
                            dict[j]=1;
            outOfRangeParam=len(dict)
            nse = totalExcursion/totalValue

            #The number of variables not meeting objectives
            f1 = (outOfRangeParam/numOfVar)*100
            #The number of tests not meeting objectives
            f2 = (outOfRangeValue/totalValue)*100
            #  excursions, their normalized sum
            f3 = nse/(0.01*nse + 0.01)
            # CCME water Quality Index
            ccmeWQI=100-(math.sqrt(pow(f1,2) + pow(f2,2) + pow(f3,2))/1.732)
            ccmedata.append({ "station" : row[0], "year" : row2[0], "ccmeWQI" : ccmeWQI, "lat" : lat, "long" : long ,"paramNum" : numOfVar } )
    db.close()
    return ccmedata

def checkRange(value, parameter):
    excursion = 0
    if parameter==2:
        if value > 3:
            excursion = (value/3)-1
            return (1,excursion)
    if parameter==3:
        if value > 5:
            excursion = (value/5)-1
            return (1,excursion)
    if parameter==4:
        if value < 7:
            excursion = (7/value)-1
            return (1,excursion)
    if parameter==5:
        if value < 50:
            excursion = (50/value)-1
            return (1,excursion)
    if parameter==6:
        if value > 35:
            excursion = (value/35)-1
            return (1,excursion)
    if parameter==7:
        if value < 12 and value > 33:
            excursion = (value/12)-1
            return (1,excursion)
    if parameter==8:
        if value > 200:
            excursion = (value/200)-1
            return (1,excursion)
    if parameter==9:
        if value > 10.5:
            excursion = (value/10.5)-1
            return (1,excursion)
    return (0,0)