#!/usr/bin/python
import rosbag

import sys
import argparse

import os
import shutil

import progressbar

import numpy as np
import cv2
from cv_bridge import CvBridge, CvBridgeError

from sensor_msgs.msg import Image


def zip_images(dir_name, output_filename):
    shutil.make_archive(output_filename, 'zip', dir_name)


def decompress_images(bag_filename, destination_folder, num_images_per_zip):

    bridge = CvBridge()
    bag = rosbag.Bag(bag_filename)

    if os.path.exists(destination_folder):
        shutil.rmtree(destination_folder)
    os.mkdir(destination_folder)

    start_time = bag.get_start_time()
    end_time = bag.get_end_time()
    run_time = end_time - start_time

    print("Bag is %.2f seconds" % run_time)

    type_topic_info = bag.get_type_and_topic_info()
    topics = type_topic_info.topics
    print("Bag contains topics: ")

    for topic in topics.keys():
        print("\t%s %s %d" % (topic, topics[topic][0], topics[topic][1]))

    toolbar_width = 70
    bar = progressbar.ProgressBar(maxval=toolbar_width,
                                  widgets=[progressbar.Bar('#', '[', ']'), ' ',
                                           progressbar.Percentage()])
    bar.start()

    num_images = 0
    subdir_names = []
    subdir_num = -1
    for topic, msg, t in bag.read_messages():
        bar.update((t.to_sec() - start_time) / run_time * toolbar_width)

        if msg._type == Image._type:

            if num_images % num_images_per_zip == 0:
                # if -1, only do this the first time
                if (num_images_per_zip != -1) or (len(subdir_names) == 0):
                    subdir_num += 1
                    subdir_names.append(
                        bag_filename.split(".")[0] + "-%s" % subdir_num)
                    os.mkdir(destination_folder + "/" + subdir_names[subdir_num])
            try:

                img = bridge.imgmsg_to_cv2(msg, desired_encoding="bgr8")
                image_name = "%s_%s.jpg" % (topic.split("/")[-1], str(t))
                destination_name = destination_folder
                destination_name += "/%s/%s" % (subdir_names[subdir_num],
                                                image_name)

                cv2.imwrite(destination_name, img)
                num_images += 1

            except CvBridgeError as e:
                print(e)

    bag.close()

    print("")  # move down a line from the progress bar
    print("Extracted %s images. Creating zips ..." % num_images)
    for subdir_name in subdir_names:
        zip_images(destination_folder + "/" + subdir_name,
                   "zipped_images/%s_unlabeled" % subdir_name)
    print("Done!")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--bag', default=None)
    parser.add_argument('--max_imgs', default=1000) # use -1 for all in one
    parser.add_argument('--output_folder', default="images")

    args = parser.parse_args(sys.argv[1:])

    if args.bag is None:
        print("Bag file is required!")
        return

    decompress_images(args.bag, args.output_folder, int(args.max_imgs))


if __name__ == "__main__":
    main()
