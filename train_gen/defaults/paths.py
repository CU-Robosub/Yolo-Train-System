"""
All paths are relative to train_gen/
"""
import os

curr_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
# curr_path = "."
zips_path = "labeled_zips/"
training_path = curr_path + "/training_data/"
data_path = training_path + "data/"
train_file = data_path + "train.txt"
test_file = data_path + "test.txt"
save_path = curr_path + "/weights_zips/"
weights_path = curr_path + "/../darknet/backup/"
train_file = data_path + "train.txt"
test_file = data_path + "test.txt"
classes_file = curr_path + "/class_names.txt"
cfg_out = "obj.data"
yolo_cfg_out = "yolov3.cfg"