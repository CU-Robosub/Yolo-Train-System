#!/usr/bin/python
import os
import shutil
from sklearn.model_selection import train_test_split

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


def create_cfg_files():
    pass


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


def image_exist():
    pass


def organize_data(path, basename, global_map, train_file, val_file):
    local_map = get_classname_mapping(basename + "/class_list.txt")

    all_names = [line.rstrip('\n') for line in open(basename + "/image_list.txt")]
    train_names, test_names = train_test_split(all_names, train_size=0.85)

    with open(path + train_file, "a") as f:
        for file in train_names:
            f.write(file + "\n")
    with open(path + val_file, "a") as f:
        for file in test_names:
            f.write(file + "\n")
    
    for img_name in os.listdir(basename + "/imgs/"):
        shutil.move(basename + "/imgs/" + img_name, path)

    for label_name in os.listdir(basename + "/labels/"):
        all_lines = [line.rstrip("\n") for line in open(basename + "/labels/" + label_name)]
        remapped_lines = [remap_class(line, global_map, local_map) for line in all_lines]
        # create new label in right spot
        with open(path + "/" + label_name, "w") as f:
            for line in remapped_lines:
                f.write(line + "\n")

        # shutil.move(basename + "/labels/" + label_name, path)
    

def main():
    print("\n")
    global_mapping = get_classname_mapping("../class_numbers.txt")

    zips_path = "labeled_zips/"
    destination_path = "training_data/"
    data_path = destination_path + "data/"

    if not os.path.exists(data_path):
        os.mkdir(data_path)

    for name in os.listdir(zips_path):
        if name.endswith(".zip"):
            print("Unzipping %s ..." % name)
            base_name = unzip_zip(zips_path, name, destination_path)
            print("Organizing data from %s ..." % name)
            organize_data(data_path, destination_path + base_name, global_mapping, "train.txt", "test.txt")
            # clean up
            shutil.rmtree(destination_path + base_name)
            print("\n")


if __name__ == "__main__":
    main()