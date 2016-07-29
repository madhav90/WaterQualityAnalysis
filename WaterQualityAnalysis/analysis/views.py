from __future__ import division
from django.shortcuts import render
from django.db import connection
import math
import json
import collections
import os.path
from django.http import HttpResponse



def index(request):
    return render(request, 'index.html', {})

def cluster(request):
    qualitydata = calculateCCMEwqi()
    return render(request, 'cluster.html',{'yearData': json.dumps(qualitydata)})

def qualityTrends(request):
    db = connection
    cursor = db.cursor()
    cursor.execute("SELECT id,stationname,latitude,longitude,sensorslist FROM stationlist")
    rows = cursor.fetchall()
    objects_list = []
    for row in rows:
        d = collections.OrderedDict()
        d['id'] = row[0]
        d['stationname'] = row[1]
        d['latitude'] = row[2]
        d['longitude'] = row[3]
        d['sensorlist'] = row[4]
        objects_list.append(d)

    j = json.dumps(objects_list)
    return render(request, 'qualitytrends.html',{'stationData': j})

def getSensorData(request):
    stationName = request.GET['station']
    print stationName
    db = connection
    cursor = db.cursor()
    cursor.execute("SELECT date,value FROM "+stationName)
    rows = cursor.fetchall()
    objects_list = []
    for row in rows:
        d = collections.OrderedDict()
        d['date'] = row[0]
        d['value'] = row[1]
        objects_list.append(d)

    j = json.dumps(objects_list)
    return HttpResponse(json.dumps(j), content_type = "application/json")

#
# def spider(request):
#     stationName = "gallinascreek"
#     data,yearData,index,indexFull,parameter = calSpiderAxis(stationName)
#     db = connection
#     cursor = db.cursor()
#     cursor.execute("select id from stationlist")
#     stationData = cursor.fetchall()
#     qualitydata=[]
#     stationParam=[]
#     yearlist=['2010','2011','2012','2013','2015','2016']
#     for station in stationData:
#         stationParam.append(station[0].encode('utf-8'))
#         print station[0]
#         data1,yearData1,qualityIndex,indexFull1,parameter1=calSpiderAxis(station[0])
#         qualitydata.append(qualityIndex)
#
#     final=[]
#     for year in yearlist:
#         wqi=[]
#         for i in range(len(qualitydata)):
#             flag=0
#             for j in range(len(qualitydata[i])):
#                 if year == qualitydata[i][j].get('year'):
#                     wqi.append(qualitydata[i][j].get('index'))
#                     flag=1
#             if flag==0:
#                 wqi.append(0)
#         print wqi
#         final.append({"name":year,"data":wqi,"pointPlacement":'on'})
#     print final
#     return render(request, 'spider.html',{'indexFull':json.dumps(indexFull),'parameter': parameter, 'qualitydata':json.dumps(final),"stationParam":stationParam})
#
# def spiderAjax(request):
#     stationName = request.GET['station']
#     print stationName
#     data,yearData,index,indexFull,parameter = calSpiderAxis(stationName)
#     print "inspiderajax"
#     j= json.dumps({'indexFull':indexFull,'parameter': parameter})
#     return HttpResponse(json.dumps(j), content_type = "application/json")
#
# def calSpiderAxis(stationName):
#     db = connection
#     cursor = db.cursor()
#     cursor.execute("select * from "+stationName)
#     spiderdataTotal=[];
#     qualityIndex=[];
#     indexFull=[]
#     parameter=[]
#     col_names = [i[0] for i in cursor.description]
#     cursor.execute("select distinct year(date) from "+stationName)
#     yearData=cursor.fetchall();
#     yearlist=[]
#
#     for year in yearData:
#         flag=0;
#         countSum=0;
#         k=str(year[0])
#         yearlist.append(k)
#         spiderdata=[]
#         indexshort=[]
#         parameterCount=0;
#         for j in col_names:
#             if(flag<3):
#                 flag=flag+1
#                 continue
#             if(j=='waterlevel'):
#                 continue
#             cursor.execute("select count(distinct "+str(j)+") from "+stationName+" where year(date)="+str(k))
#             data1 = cursor.fetchall()
#             for row1 in data1:
#                 if(row1[0]!=0):
#                     parameterCount+=1
#                 break
#         flag=0;
#         print "parameterCount"
#         print parameterCount
#         for i in col_names:
#             if(flag<3):
#                 flag=flag+1
#                 continue
#             if(i=='waterlevel'):
#                 continue
#             parameter.append(i)
#
#             cursor.execute("select "+i+" from "+stationName+" where year(date)="+k)
#             data = cursor.fetchall()
#             goodCount=0;
#             totalCount=0;
#             sum =0;
#             for row in data:
#                 if row[0] == None:
#                     continue
#                 count,deviation=checkSensorRange(i,row[0])
#                 goodCount += count
#                 totalCount=totalCount+1
#                 sum += deviation
#             if(totalCount==0):
#                 countPercent=0
#                 avgDeviation=0
#             else:
#                 countPercent = (goodCount*100)/totalCount
#                 avgDeviation = sum/totalCount
#             countSum += countPercent
#             spiderdata.append({ "axis" :i, "value" : countPercent} )
#             indexshort.append(countPercent)
#         if parameterCount!=0:
#             countAvg = countSum/parameterCount
#         else:
#             countAvg=0
#         qualityIndex.append({"year":k, "index":countAvg})
#         spiderdataTotal.append(spiderdata)
#         indexFull.append({"name":k,"data":indexshort,"pointPlacement":'on'})
#     return spiderdataTotal,yearlist,qualityIndex,indexFull,parameter
#
#
# def checkSensorRange(parameter,value):
#     deviation=0
#     count=0
#     if(parameter=='do'):
#         if value < 70:
#             deviation = abs(value-70)
#         else:
#             count += 1
#             deviation=0
#     elif(parameter =='ph'):
#         if value < 6.5:
#             deviation = 6.5-value
#         elif value > 8.5:
#             deviation = value-8.5
#         else:
#             count += 1
#             deviation=0
#     elif(parameter=='salinity'):
#         if value > 30:
#             deviation = value-30
#         else:
#             count += 1
#             deviation=0
#     elif(parameter=='turbidity'):
#         if value > 50:
#             deviation = value-50
#         else:
#             count += 1
#             deviation=0
#     elif(parameter=='chlorophyll'):
#         if value > 3:
#             deviation = value-3
#         else:
#             count += 1
#             deviation=0
#     elif(parameter=='temp'):
#         if value < 55:
#             deviation = 55-value
#         elif value>90:
#             deviation = value-90
#         else:
#             count += 1
#             deviation=0
#     else:
#         print("no parameter")
#         print value
#     return(count, deviation)


def calculateCCMEwqi():
    db = connection
    cursor = db.cursor()
    cursor.execute("SELECT distinct(station) from usgsdata")
    data = cursor.fetchall()
    ccmedata=[];

    for row in data:
        cursor.execute("select * from usgsdata group by station having station=" + row[0])
        data1 = cursor.fetchone()
        col = [i[0] for i in cursor.description]
        cursor.execute("select latitude,longitude from usgs_station where station=" + row[0])
        coordinate = cursor.fetchone()
        if(coordinate == None):
            continue
        lat = coordinate[0]
        long = coordinate[1]
        numOfVar = 0
        numVar= []
        for i in range(2,10):
            if data1[i] != None:
                numOfVar += 1
                numVar.append(col[i])
        print numVar
        cursor.execute("select distinct year(date) from usgsdata where station=" + row[0])
        data2 = cursor.fetchall();
        for row2 in data2:
            k= str(row2[0])
            cursor.execute("select * from usgsdata where station=" + row[0] + " and year(date)=" + k)
            col_names = [i[0] for i in cursor.description]
            data3=cursor.fetchall();
            outOfRangeValue = 0;
            totalValue=0;
            totalExcursion=0;
            dict={};
            outParam=[];
            for row3 in data3:
                for j in range(2,10):
                    if row3[j] != None:
                        totalValue += 1
                        flag,excursion = checkRange(row3[j],j)
                        totalExcursion += excursion
                        if flag == 1:
                            outOfRangeValue +=1
                            dict[col_names[j]]=1;
            for key in dict:
                outParam.append(key)
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
            ccmedata.append({ "station" : row[0], "year" : row2[0], "ccmeWQI" : ccmeWQI, "lat" : lat, "long" : long ,"paramNum" : numOfVar,
                              "outParam" : outParam, "paramUsed" : numVar} )
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

def kmeans(request):
    return render(request, 'kmeans.html', {})