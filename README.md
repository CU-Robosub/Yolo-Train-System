# Yolo Train System

This repo helps automate the process of deploying a new neural net to the sub, all the way from data collection to training and exporting.

The process:
- Obtain bag files -> upload to Drive with correct name format: C###_M-dd-YY(#)-#.bag (see [naming](https://docs.google.com/document/d/11Dcfjjd2715yeOiL1VhgAn_CUhakEOS4rWTMpqKFxYM/edit))
- Download bag file to data_gen/
- Run bag_to_images.py:
```
cd data_gen/
python bag_to_images.py --bag=<filename>.bag
```
- Now, the most fun part, label images: `python OpenLabeling/main/main.py`
- Zip labels and images together: `python OpenLabeling/main/labeled_to_zip.py` -> upload to Drive
- Download all labeled zips to train_gen/labeled_zips/
- Prepare data for darknet: `python zips_to_train_set.py`
- Train the net. From the darknet folder: `./darknet detector train ../train_gen/obj.data ../train_gen/yolov3.cfg darknet53.conv.74 -map`
- ... A few hours later, organize the weights: `python zip_weights.py` -> upload to Drive