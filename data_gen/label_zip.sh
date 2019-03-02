#!/usr/bin/env bash

num=`ls -l zipped_images/ | wc -l`
if [ $num -lt 2 ]
then
    echo "No zips located in zipped_images. Exiting"
    exit
fi

num=`ls -l OpenLabeling/main/input/ | wc -l`
if [ $num -ne 1 ]
then
    echo "OpenLabeling directory currently contains images. Please enter OpenLabeling/main and run labeled2zip.sh to save and clear these images if they are already labeled."
    exit
fi

cd zipped_images
zip_arr=(*.zip)
index=0
echo "Please select a zip file to move to OpenLabeling"
for i in ${zip_arr[@]}; do
    echo "["$index"] : "$i
    index=$((index+1))
done
read res

echo "Selected "${zip_arr[$res]}

cp ${zip_arr[$res]} ../OpenLabeling/main/input/
cd ../OpenLabeling/main/input
unzip ${zip_arr[$res]}
rm ${zip_arr[$res]}
num_images=`ls -l |wc -l`
cd ../../../
#echo ${zip_arr[$res]}
echo "Unzipped and loaded "$num_images" images into OpenLabeling."
echo "---------------------------"
echo "Would you like to start labeling? [y/n]"
read labeling_answer
if [ "$labeling_answer" = "y" ]
then
    cd OpenLabeling/main
    python main.py
fi
