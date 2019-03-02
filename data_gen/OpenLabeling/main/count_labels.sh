#!/usr/bin/env bash
# Input zip file -> output the following
# Class 1 : num
# Class 2 : num
# Class 3 : num
# Class 4 : num
# ...
# Class n : num

if [ -z $1 ]
then
    echo "You must pass in a zip file"
    exit
fi

mkdir tmp_zip_dir
cp $1 tmp_zip_dir/
cd tmp_zip_dir
echo "Unzipping..."
unzip -q $1

class_counts=()
cls=0
while read p; do
    class_counts[$cls]=0
    ((cls++))
done < class_list.txt

cd labels
for f in $(ls); do
    while read p; do
	arr=( $p )
	cls=${arr[0]} # get the class
	((class_counts[$cls]++))
    done <$f
done

cd ..

# Print the results
index=0
while read p; do
    echo "$p : "${class_counts[$index]}
    ((index++))    
done < class_list.txt

cd ..
rm -r tmp_zip_dir
