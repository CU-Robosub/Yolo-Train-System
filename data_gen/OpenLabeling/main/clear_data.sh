#!/usr/bin/env bash
echo "Are you sure you would like to clear all data? [y/n]"
read answer
if [ "$answer" = "y" ]
then
    rm input/*
    rm output/YOLO_darknet/*
    rm output/PASCAL_VOC/*
fi
