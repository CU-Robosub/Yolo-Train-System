#!/usr/bin/python

import matplotlib.pyplot as plt
import os
# from ..defaults import paths 

def get_class_map(filename):
    mapping = {}
    all_lines = [line.rstrip("\n") for line in open(filename)]
    for i, line in enumerate(all_lines):
        line = line.split(" ")
        if len(line) == 2:
            mapping[int(line[0])] = {}
            mapping[int(line[0])]["name"] = line[1]
        elif len(line) == 1:
            mapping[i] = {}
            mapping[i]["name"] = line[0]
        else:
            raise ValueError("Could not read classes!")

    return mapping

def main():
    class_map = get_class_map("../class_names.txt")
    
    for class_idx in class_map:
        class_map[class_idx]["count"] = 0
    
    data_path = "../training_data/data/"
    all_names = [name for name in os.listdir(data_path) if name.endswith(".txt")]

    for name in all_names:
        if "train" in name or "test" in name: # don't count these
            continue
        all_lines = [line.rstrip("\n") for line in open(data_path + name)]
        for line in all_lines:
            class_map[int(line[0])]["count"] += 1

    print(class_map)
    xs = []
    ys = []
    labels = []

    for class_idx in class_map:
        xs.append(class_idx)
        ys.append(class_map[class_idx]["count"])
        labels.append(class_map[class_idx]["name"])


    fig, ax = plt.subplots()
    ax.yaxis.grid(True)
    ax.set_axisbelow(True)
    plt.bar(xs, ys)
    plt.xticks(xs, labels)
    plt.title("Training Data Visualization")
    plt.xlabel("Classname")
    plt.ylabel("# of Labeled Images")
    plt.show()

if __name__ == "__main__":
    main()