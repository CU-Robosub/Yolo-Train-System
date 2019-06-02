#!/usr/bin/python
"""
This script takes any zipped labeled sets in labeled_zips/ and adds them to the 
master training set in training_data/data/. It does a few things:
- Adds all images to training_data/data/
- Uses the global class_numbers file to remap indicies in the labeled set to 
the correct global index of each class, based on the name
- Writes the correct label file to training_data/data/
- Does a random 85/15 train/val split and adds the filenames to
training_data/data/train.txt and training_data/data/test.txt

TODO: 
- check if image exists, and if it does, skip it. this would allow for overlap
in labeled datasets


"""
import os
import shutil
from sklearn.model_selection import train_test_split
from string import Template

def get_classname_mapping(filename):
    mapping = {}
    all_lines = [line.rstrip("\n") for line in open(filename)]
    for i, line in enumerate(all_lines):
        line = line.split(" ")
        if len(line) == 2:
            mapping[int(line[0])] = line[1]
        elif len(line) == 1:
            mapping[i] = line[0]
        else:
            raise ValueError("Could not read classes!")

    return mapping


def get_basename(zip_name):
    return zip_name.replace(".zip", "")


def unzip_zip(path, zip_name, target_folder):
    sub_folder = get_basename(zip_name)
    shutil.unpack_archive(path + zip_name, target_folder + "/" + sub_folder, "zip")

    return sub_folder


def generate_template(infile, outfile, values):
    cfg_file = Template(open(infile).read())
    output = cfg_file.substitute(values)
    with open(outfile, "w") as f:
        f.write(str(output))


def create_cfg_file(cfg_template, cfg_output, num_classes, train_file, valid_file, names_file, weights_dir):    
    values = {  "num_classes" : num_classes,
                "train_file"  : train_file,
                "valid_file"  : valid_file,
                "names_file"  : names_file,
                "backup_dir"  : weights_dir }
    
    generate_template(cfg_template, cfg_output, values)

def create_yolo_cfg_file(yolo_template, yolo_output, num_classes):
    max_batches = num_classes * 2000
    steps1 = int(max_batches * 0.8)
    steps2 = int(max_batches * 0.9)
    num_filters = (num_classes + 5) * 3

    values = {  "num_classes" : num_classes,
                "max_batches" : max_batches,
                "steps1"      : steps1,
                "steps2"      : steps2,
                "num_filters" : num_filters }
    
    generate_template(yolo_template, yolo_output, values)


def remap_class(line, target_map, current_map):
    split_line = line.split(" ")
    this_class = current_map[int(split_line[0])]
    for class_id in target_map:
        if target_map[class_id] == this_class:
            break
    
    split_line[0] = class_id

    return_str = ""
    for i, item in enumerate(split_line):
        return_str += str(item)
        if i != len(split_line) - 1:
            return_str += " "

    return return_str

# TODO
def image_exist():
    pass


def organize_data(path, basename, global_map, train_file, val_file):
    local_map = get_classname_mapping(basename + "/class_list.txt")

    # move all files
    for img_name in os.listdir(basename + "/imgs/"):
        shutil.move(basename + "/imgs/" + img_name, path)

    for label_name in os.listdir(basename + "/labels/"):
        all_lines = [line.rstrip("\n") for line in open(basename + "/labels/" + label_name)]
        remapped_lines = [remap_class(line, global_map, local_map) for line in all_lines]
        # create new label in right spot
        with open(path + "/" + label_name, "w") as f:
            for line in remapped_lines:
                f.write(line + "\n")

    all_names = [line.rstrip('\n') for line in open(basename + "/image_list.txt")]
    train_names, test_names = train_test_split(all_names, train_size=0.85)

    with open(train_file, "a") as f:
        for file in train_names:
            f.write(path + file + "\n")
    with open(val_file, "a") as f:
        for file in test_names:
            f.write(path + file + "\n")
    

def main():
    # hard coded names
    curr_path = os.path.dirname(os.path.abspath(__file__))
    zips_path = "labeled_zips/"
    destination_path = curr_path + "/training_data/"
    data_path = destination_path + "data/"
    train_file = data_path + "train.txt"
    test_file = data_path + "test.txt"
    classes_file = curr_path + "/class_names.txt"
    cfg_template = "obj.data.in"
    cfg_out = "obj.data" # TODO: move once model_gen is correct
    yolo_cfg_template = "yolov3.cfg.in"
    yolo_cfg_out = "yolov3.cfg" # TODO: move once model_gen is correct

    print("\n")

    global_mapping = get_classname_mapping(classes_file)

    if not os.path.exists(data_path):
        os.mkdir(data_path)

    for name in os.listdir(zips_path):
        if name.endswith(".zip"):
            print("Unzipping %s ..." % name)
            base_name = unzip_zip(zips_path, name, destination_path)
            print("Organizing data from %s ..." % name)
            organize_data(data_path, destination_path + base_name, global_mapping, train_file, test_file)
            # clean up
            shutil.rmtree(destination_path + base_name)
            print("\n")

    print("Generating config files ...\n")
    create_cfg_file(cfg_template, "obj.data", len(global_mapping), train_file, test_file, classes_file, "backup/")
    create_yolo_cfg_file(yolo_cfg_template, yolo_cfg_out, len(global_mapping))


if __name__ == "__main__":
    main()