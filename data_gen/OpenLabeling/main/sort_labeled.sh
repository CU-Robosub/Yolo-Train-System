#!/usr/bin/env bash

mkdir -p positives/labels
mkdir -p positives/imgs
mkdir -p negatives/labels
mkdir -p negatives/imgs

for i in $(ls output/YOLO_darknet); do
    content=`cat output/YOLO_darknet/$i`
    root_name=${i::-4}
    if [ -z "$content" ]; then
	cp output/YOLO_darknet/$i negatives/labels/$i
	cp input/$root_name.jpg negatives/imgs/$root_name.jpg
    else
	cp output/YOLO_darknet/$i positives/labels/$i
	cp input/$root_name.jpg positives/imgs/$root_name.jpg	
    fi
done
