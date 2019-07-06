#!/usr/bin/python
"""
This script checks the backup folder in darknet for weights and organizes into a
zip that can be uploaded to google drive, formatted correctly

TODO:
    - automatically fill in README in the zip using the info in the labels,
    for now it'll be input at the console
"""
import os
import shutil
import zipfile
import datetime

from defaults import paths

def main():
    # hard coded names
    zip_name = "darknet_training_"
    zip_name += '{0:%m-%d-%Y}'.format(datetime.datetime.now())
    zip_folder = paths.weights_path + zip_name + "/"
    weights_destination_path = zip_folder + "/weights/"
    weights_destination_backup_path = zip_folder + "/weights/backup/"

    print("\n")

    # create structure
    os.mkdir(zip_folder)
    os.mkdir(weights_destination_path)
    os.mkdir(weights_destination_backup_path)

    # get any training notes 
    readme_info = input("Enter any notes on the training:\n")

    with open(zip_folder + "README.txt", "w") as f:
        f.write(readme_info)
        f.write("\n")

    shutil.move(paths.weights_path + "../chart.png", zip_folder)

    tiny_yolo = False
    for name in os.listdir(paths.weights_path):
        if name.endswith(".weights"):
            print("Adding %s ..." % name)
            
            if "best" in name:
                shutil.copy(paths.weights_path + name, weights_destination_path)
            else:
                shutil.copy(paths.weights_path + name, weights_destination_backup_path)

            if "tiny" in name and not tiny_yolo:
                tiny_yolo = True

    # add extra config files
    shutil.copy(paths.cfg_out, zip_folder)
    shutil.copy(paths.classes_file, zip_folder)
    shutil.copy(paths.train_file, zip_folder)
    shutil.copy(paths.test_file, zip_folder)

    if tiny_yolo:
        yolo_cfg = "yolov3-tiny.cfg"
    else:
        yolo_cfg = "yolov3.cfg"

    shutil.copy(yolo_cfg, zip_folder)


    # move out of darknet
    shutil.move(zip_folder, paths.save_path + zip_name)

    print("\nDone! %s is ready to upload\n"%(paths.save_path + zip_name).replace(paths.curr_path, ""))
    

if __name__ == "__main__":
    main()