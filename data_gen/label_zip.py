#!/usr/bin/env python
import os
import shutil
import zipfile

def unzip_zip(path, zip_name, target_folder):
    zip_ref = zipfile.ZipFile(path + zip_name, 'r')
    zip_ref.extractall(target_folder)
    zip_ref.close()

    print(zip_name)

    # return sub_folder

def get_zips(path):
    return [name for name in os.listdir(path) if name.endswith("zip")]

def main():
    path = "zipped_images/"
    open_labeling_path = "OpenLabeling/main/"
    target_input_folder = open_labeling_path + "input/"
    target_output_folder = open_labeling_path + "output/"
    
    if not os.path.exists(target_input_folder):
        os.mkdir(target_input_folder)
        os.mkdir(target_output_folder)
    else:
        if len(os.listdir(target_input_folder)) > 0 or len(os.listdir(target_output_folder)) > 0:
            print("\nError! files exist in OpenLabeling, run labeled_to_zip.py")
            exit(-1)

    zips = get_zips(path)
    print("Select zip to label:")
    for i, zip_file in enumerate(zips):
        print("[%s]: %s"%(i, zip_file))

    zip_num = input()
    zip_num = int(zip_num)

    unzip_zip(path, zips[zip_num], target_input_folder)
    
    with open(open_labeling_path + "current_zip.txt", "w") as f:
        f.write(zips[zip_num] + "\n")
    
    shutil.copy("../train_gen/class_names.txt", open_labeling_path + "class_list.txt")

    print("Done! Ready to run OpenLabeling\n")


if __name__ == '__main__':
    main()