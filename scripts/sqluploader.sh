#!/bin/bash

echo "Inserting Data into MySQL"


filenames=( *.csv )

echo "Totalnumber of csv files"
echo ${#filenames[@]} # will echo number of elements in array

# echo "${filenames[@]}" # will dump all elements of the array

for z in "${!filenames[@]}"
do
# echo ${z%%.*}
filenames[z]=${filenames[$z]%.*}

# echo "${filenames[@]}"

done


for i in "${filenames[@]}"
do
# echo $filenames

echo "CREATE TABLE IF NOT EXISTS $i ( date VARCHAR(10) NOT NULL, value FLOAT);" | mysql -u root -proot waterquality;

# done

# for j in "${noextension[@]}"
# do

echo "TRUNCATE TABLE $i;" | mysql -u root -proot waterquality;

echo "CREATE INDEX $i ON $i (date,value);" | mysql -u root -proot waterquality;

IFS=,
while read 'date' 'value'
      do
        echo "INSERT INTO $i (date,value) VALUES ('$date', '$value');"

done < $i.csv | mysql -u root -proot waterquality;

# unset IFS


done