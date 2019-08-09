import os, io, sys, shutil
from zipfile import ZipFile
import rospkg
import yaml

def findWeight():
	current_wd = os.getcwd()
	darknetTrainings = []
	weight_filename = ""
	index = 0
	print("***")
	for filename in os.listdir(current_wd):
		if "darknet" in filename:
			darknetTrainings.append(filename)
			print("[" + str(index) + "] : " + str(filename))
			index += 1
	print("***")
	darknetTrainingsIndex = raw_input("Choose Weight File: ")
	filename = darknetTrainings[int(darknetTrainingsIndex)]
	print("You have selected: " + filename)
	print
	transferInfo(filename)


def transferInfo(folder_name):
	# Add yolov3 cfg to darknet_config cfg directory
	current_wd = os.getcwd()
	download_dir_path = current_wd + "/" + str(folder_name)
	rospack = rospkg.RosPack()
	darknet_config_path = rospack.get_path('darknet_config')
	os.chdir(darknet_config_path)
	os.chdir("./cfg")
	cfg_filename = "yolov3-tiny.cfg"
	for filename in os.listdir(download_dir_path):
		if "yolov3" in str(filename):
			cfg_filename = filename
	first_dir = download_dir_path + "/" + str(cfg_filename)
	second_dir = darknet_config_path + "/cfg/" + str(cfg_filename)
	if os.path.exists(cfg_filename):
		os.remove(cfg_filename)
		print(cfg_filename + " has been replaced in " + darknet_config_path + "/cfg/")
	else:
		print(cfg_filename + " has been added to " + darknet_config_path + "/cfg/")
	shutil.move(first_dir, second_dir)
	print

	# CONSULTING THE CHART BOIII
	chartInput = raw_input("[1] Consult Chart, [any other char] Don't Consult Chart: ")
	print
	os.chdir(download_dir_path)
	if chartInput == "1":
		os.system("xdg-open chart.png")

	# # Moves content from backup to weight directory
	index = 0
	weightNames = []
	weight_filename = ""
	weight_choice = raw_input("[1] Select best.weights, [any other char] View Backup Directory: ")
	if weight_choice == "1":
		weight_filename = "yolov3-tiny_best.weights"
		for filename in os.listdir((download_dir_path + "/weights/")):
			if "yolov3" in filename:
				weight_filename = filename
		first_dir = download_dir_path + "/weights/" + weight_filename
		second_dir = darknet_config_path + "/weights/" + weight_filename
	else:
		print("***")
		for filename in os.listdir(download_dir_path + "/weights/backup"):
			weightNames.append(filename)
			print("[" + str(index) + "] : " + str(filename))
			index += 1
		print("***")
		weightNamesIndex = raw_input("Choose Weight File: ")
		filename = weightNames[int(weightNamesIndex)]
		print("You have selected: " + filename)
		first_dir = download_dir_path + "/weights/backup/" + str(filename)
		second_dir = darknet_config_path + "/weights/" + str(filename)
		weight_filename = filename
	os.chdir(darknet_config_path + "/weights/")
	if os.path.exists(weight_filename):
		os.remove(weight_filename)
		print(weight_filename + " has been replaced in " + darknet_config_path + "/weights/")
	else:
		print(weight_filename + " has been added to " + darknet_config_path + "/weights/")
	shutil.move(first_dir, second_dir)
	print


	# # Modify YAML file to change names and weight file chosen
	os.chdir(download_dir_path)
	with open('class_names.txt') as file1:
		yaml_names_arr = file1.readlines()
		yaml_names_arr = [line.rstrip('\n') for line in open('class_names.txt')]
	yolov3_yaml = {'yolo_model': {'threshold': {'value': 0.3}, 'detection_classes': {'names': yaml_names_arr}, 'weight_file': {'name': weight_filename}, 'config_file': {'name': cfg_filename}}}
	os.chdir(darknet_config_path)
	os.chdir("./yaml")
	yaml_file_name = "yolov3-tiny.yaml"
	if ("-tiny" not in str(weight_filename)) and ("-tiny" not in str(cfg_filename)):
		yaml_file_name = "yolov3.yaml"
	elif ("-tiny" in str(weight_filename)) and ("-tiny" in str(cfg_filename)):
		yaml_file_name = "yolov3-tiny.yaml"
	else:
		print("cfg: " + cfg_filename)
		print("weight: " + weight_filename)
		print("CANNOT HAVE YOLO-FULL & YOLO-TINY CONFLICTING FILES")
		yaml_file_name = "shiz"
	if "shiz" not in yaml_file_name:
		print("YAML FILE NAME: " + yaml_file_name)
		os.remove(yaml_file_name)
		with open(yaml_file_name, "w") as file2:
			yaml.dump(yolov3_yaml, file2, default_flow_style=False)

findWeight()