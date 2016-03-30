import os
import csv
from collections import defaultdict
from cassandra.cluster import Cluster

cluster = Cluster()
session = cluster.connect('waterquality')

for name in os.listdir('/Users/dolly/Desktop/Data'):
    if name != '.DS_Store':
        print name + '---------------------'
        for param in os.listdir('/Users/dolly/Desktop/Data/'+name):
            if param != '.DS_Store':
                print param
                filename = '/Users/dolly/Desktop/Data/'+name+'/'+param+'/data.csv'
                with open(filename, 'rb') as csvfile:
                    csvfile.readline();
                    reader = csv.reader(csvfile, delimiter=',')
                    data = defaultdict(list)
                    for row in reader:
                        dateString = row[4]
                        date = dateString[:10]
                        value = row[5]
                        try:
                            fvalue = float(value)
                        except ValueError,e:
                            print "error",e,"on value"+value+"  "+date
                            continue
                        data[date].append(fvalue)
                    for date, value in data.iteritems():
                        processedValue=sum(value)/ float(len(value))
                        session.execute("insert into data (station_id, parameter, date, value)values('"+name+"','"+param+"','"+date+"',"+str(processedValue)+");")
cluster.shutdown()



