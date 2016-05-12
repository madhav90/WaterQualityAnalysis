#!/bin/bash


# MY_VARIABLE=10

# echo $MY_VARIABLE




# echo "Hello World"

# function hello {
# echo hello
# }

# hello



# 20706 
echo "Downloading and Processing Data Files"


stations=( 'chinacamp' 'gallinascreek' 'tiburon' 'carquinez' 'fortpoint' 'sfbaypier17a' 'sfbaysanmateobridge' 'sfbaydumbartonbridge' )
sensors=( 'temp' 'do' 'salinity' 'chlorophyll' 'turbidity' 'ph' 'waterlevel' )

for i in "${stations[@]}"
do

if [[ $i == 'chinacamp' ]]
	then
	STATIONID='stationid=18432'
fi
if [[ $i == 'gallinascreek' ]]
	then
	STATIONID='stationid=18436'
fi
if [[ $i == 'tiburon' ]]
	then
	STATIONID='stationid=20358'
fi
if [[ $i == 'carquinez' ]]
	then
	STATIONID='stationid=20365'
fi
if [[ $i == 'fortpoint' ]]
	then
	STATIONID='stationid=20364'
fi
if [[ $i == 'sfbaypier17a' ]]
	then
	STATIONID='stationid=20706'
fi
if [[ $i == 'sfbaysanmateobridge' ]]
	then
	STATIONID='stationid=20708'
fi
if [[ $i == 'sfbaydumbartonbridge' ]]
	then
	STATIONID='stationid=32599'
fi

for j in "${sensors[@]}"
do

# echo $j
if [[ $j == 'temp' ]]
	then
	SENSORID='&sensorid=7&version=2&units=42;degree_Fahrenheit,41;degree_Fahrenheit'
fi
if [[ $j == 'do' ]]
	then
	SENSORID='&sensorid=35&version=2&units=81;1e-6,80;'
fi
if [[ $j == 'salinity' ]]
	then
	SENSORID='&sensorid=14&version=2&units=50;1e-3'
fi
if [[ $j == 'chlorophyll' ]]
	then
	SENSORID='&sensorid=41&version=2&units=89;microg.L-1'
fi
if [[ $j == 'turbidity' ]]
	then
	SENSORID='&sensorid=37&version=2&units=83;ntu'
fi
if [[ $j == 'ph' ]]
	then
	SENSORID='&sensorid=36&version=2&units=82;1'
fi
if [[ $j == 'waterlevel' ]]
	then
	SENSORID='&sensorid=25&version=2&units=46;ft'
fi

UNIXEPOCH="$(date +'%s')"
# echo $UNIXEPOCH



#http://pdx.axiomalaska.com/stationsensorservice/getExcelSheet?stationid=20708&sensorid=7&version=2&units=42;degree_Fahrenheit,41;degree_Fahrenheit&start_time=1414800000&end_time=1460595600



BASEURL='http://pdx.axiomalaska.com/stationsensorservice/getExcelSheet?'
# STATIONID='stationid='$i
# SENSORID='&sensorid=7&version=2&units=42;degree_Fahrenheit,41;degree_Fahrenheit'
STARTTIME='&start_time=0'
ENDTIME='&end_time='$UNIXEPOCH

URL=$BASEURL$STATIONID$SENSORID$STARTTIME$ENDTIME
FILENAME=$i$j
# echo $URL

# mkdir -p /tmp/some_tmp_dir                         && \
# cd /tmp/some_tmp_dir                            && \
# curl -sS http://foo.bar/filename.zip > file.zip && \
curl -sS $URL > file.zip && \
unzip -oqq file.zip                                  && \
rm -f file.zip                                  && \
rm -f metadata.txt                                  && \
# mv data.csv $FILENAME.csv                                  && \
sed 1d data.csv > datatemp.csv 2>/dev/null                                  && \
cut -d, -f5,6 datatemp.csv > datatemp2.csv                                  && \
sed -e 's/\(T\).*\(Z\)/\1\2/' datatemp2.csv > datatemp3.csv                                    && \
sed 's/TZ//' datatemp3.csv > datatemp4.csv                                  && \
awk 'BEGIN{FS=",";} NR!=1 {a[$1]++;b[$1]=b[$1]+$2}END{for (i in a) printf("%s,%10.2f\n", i, b[i]/a[i])} ' datatemp4.csv > $FILENAME.csv
sort -n -o $FILENAME.csv $FILENAME.csv 2>/dev/null
# mv datatemp5.csv $FILENAME.csv 2>/dev/null                                  && \
rm -f data.csv                                  && \
rm -f datatemp.csv                                  && \
rm -f datatemp2.csv                                  && \
rm -f datatemp3.csv                                  && \
rm -f datatemp4.csv                                  && \
rm -f Error.csv

done
done

rm -f file.zip                                  && \
rm -f metadata.txt                                  && \
rm -f data.csv                                  && \
rm -f datatemp.csv                                  && \
rm -f datatemp2.csv                                  && \
rm -f datatemp3.csv                                  && \
rm -f datatemp4.csv                                  && \
rm -f Error.csv



# #To delete the zero byte files created due to sort
# #need to find a better solution
# i=100
# while [ $i -le 999 ];do
#     rm -f file${i}*;
#     let i++;
# done