#!/usr/bin/env bash

# For unlabeled zip archives containing greater than UNLABELED_ZIP_MAX_SIZE jpgs, split the jpgs into multiple zip archives to allow team members to label the data concurrently

UNLABELED_ZIP_MAX_SIZE=1000

if [ -z $1 ]
then
    echo "You must pass in an unlabeled zip file"
    exit
fi

cur_dir=`ls |grep bag2images`
if [ -z "$cur_dir" ]
then
    echo "This script must be run from the data_gen directory: ./scripts/split_unlabeled.sh /path/to/zip"
    exit
fi


# Get the count of the bag file
mkdir -p zipped_images/tmp
mv $1 zipped_images/tmp
cd zipped_images/tmp
unzip *
num_files=`ls -l |wc -l`
echo "Number of files: "$num_files



mv *.zip ../
cd ../../

rm -r zipped_images/tmp
