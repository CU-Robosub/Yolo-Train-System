#!/usr/bin/env bash

cd output/YOLO_darknet # just change this line herex


for i in $(ls); do
    echo $i
    mv $i C0_${i#*_}
#    echo $new_str
#    echo "${i#*_}"
done
