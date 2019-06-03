#!/usr/bin/env python
import os
import shutil


def sort_labeled(input_dir, output_dir, positive_dir, negative_dir):
    positive_images = []
    negative_images = []
    for file in os.listdir(output_dir):
        with open(output_dir + file) as f:
            lines = 0
            for _ in f:
                lines += 1

            base_name = file.replace(".txt", "")
            # contains a label
            if lines > 0:
                shutil.move(output_dir + file, positive_dir + "labels/" + file)
                shutil.move(input_dir + base_name + ".jpg", positive_dir
                            + "imgs/" + base_name + ".jpg")
                positive_images.append(base_name + ".jpg")
            # contains no label
            else:
                shutil.move(output_dir + file, negative_dir + "labels/" + file)
                shutil.move(input_dir + base_name + ".jpg", negative_dir
                            + "imgs/" + base_name + ".jpg")
                negative_images.append(base_name + ".jpg")

    print("Found %s positives and %s negatives" % (len(positive_images),
                                                   len(negative_images)))

    # add class names to archive
    shutil.copy("class_list.txt", positive_dir)
    shutil.copy("class_list.txt", negative_dir)

    # add all image names to archive
    with open(positive_dir + "image_list.txt", "a") as f:
        for img in positive_images:
            f.write(img + "\n")

    with open(negative_dir + "image_list.txt", "a") as f:
        for img in negative_images:
            f.write(img + "\n")


def zip_labeled(positive_dir, negative_dir, zip_name):
    pos_zip = zip_name
    neg_zip = "negatives-" + zip_name

    shutil.make_archive(zip_name, "zip", positive_dir)
    shutil.make_archive(neg_zip, "zip", negative_dir)

    return pos_zip + ".zip", neg_zip + ".zip"


def main():
    # setup
    os.mkdir("positives")
    os.mkdir("positives/imgs")
    os.mkdir("positives/labels")
    os.mkdir("negatives")
    os.mkdir("negatives/imgs")
    os.mkdir("negatives/labels")

    print("\nSorting labels ...")
    sort_labeled("input/", "output/YOLO_darknet/", "positives/", "negatives/")

    print("Zipping data ...")
    zip_name = "UNKNOWN-ZIPNAME"
    with open("current_zip.txt") as f:
        zip_name = f.readline().replace("\n", "")
        zip_name = zip_name.replace("_unlabeled.zip", "")

    pos_zip, neg_zip = zip_labeled("positives", "negatives", zip_name)

    print("Done! %s and %s created\n" % (pos_zip, neg_zip))

    # clean up
    shutil.rmtree("positives")
    shutil.rmtree("negatives")

    shutil.rmtree("output")
    os.mkdir("output")


if __name__ == "__main__":
    main()
