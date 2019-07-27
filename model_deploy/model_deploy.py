from __future__ import print_function
import httplib2
import os, io, sys, shutil
from zipfile import ZipFile
import rospkg
import yaml

from apiclient import discovery
from apiclient import errors
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage
from apiclient.http import MediaFileUpload, MediaIoBaseDownload
try:
    import argparse
    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None
import auth
# If modifying these scopes, delete your previously saved credentials
# at ~/.credentials/drive-python-quickstart.json
SCOPES = 'https://www.googleapis.com/auth/drive'
CLIENT_SECRET_FILE = 'client_secret.json'
APPLICATION_NAME = 'model_deploy'
authInst = auth.auth(SCOPES,CLIENT_SECRET_FILE,APPLICATION_NAME)
credentials = authInst.getCredentials()

http = credentials.authorize(httplib2.Http())
drive_service = discovery.build('drive', 'v3', http=http)

def searchFile(queryFileName):
    # query = "mimeType = 'application/x-zip-compressed' and name contains '%s'" % queryFileName
    query1 = "mimeType = 'application/vnd.google-apps.folder' and name contains '%s'" % queryFileName
    results1 = drive_service.files().list(q=query1).execute()
    items1 = results1.get('files', [])
    items1 = items1[:10]
    fileIndex = 0
    if not items1:
        print('No Drive Folders found.')
        print()
    else:
        print('Drive Folder(s):')
        for item in items1:
            print("[" + str(fileIndex) + "]" + ' {0} ({1})'.format(item['name'], item['mimeType']))
            fileIndex += 1
        print()
    downloadInput = raw_input("Select weight file to download: ")
    chosenItem = items1[int(downloadInput)]
    folder_id = chosenItem['id']
    file_name = chosenItem['name']
    print("Downloading: " + str(file_name) + "...")
    return_tuple = (folder_id, file_name)
    return(return_tuple)


def downloadFile(file_id,filepath):
    request = drive_service.files().get_media(fileId=file_id)
    fh = io.BytesIO()
    downloader = MediaIoBaseDownload(fh, request)
    done = False
    while done is False:
        status, done = downloader.next_chunk()
        # print("Download %d%%." % int(status.progress() * 100))
    with io.open(filepath,'wb') as f:
        fh.seek(0)
        f.write(fh.read())

def download_files_in_folder(folder_id):
    query = "'%s' in parents" % folder_id
    children = drive_service.files().list(q=query).execute()
    child_list = children[u'files']
    download_index = 1
    stepCount = 0
    for item in child_list:
        mimetype = item[u'mimeType']
        name = item[u'name']
        id = item[u'id']
        if "folder" not in mimetype:
            print(" Downloading file " + str(download_index) + " of " + str(len(child_list)) + "...")
            download_index += 1
            downloadFile(id, name)
        else:
            print(" *%s*" % name)
            os.system("mkdir %s" % name)
            dir = str(os.getcwd()) + "/" + name
            os.chdir(dir)
            download_files_in_folder(id)
            os.system("cd ..")


def searchAndDownloadWeight():
    parametersFile = open("parameters.txt", "r")
    line = parametersFile.readline()
    parameters = line.split(".")
    searchName = parameters[0]

    (folder_id, folder_name) = searchFile(searchName)
    os.system("mkdir %s" % folder_name)
    dir = str(os.getcwd()) + "/" + folder_name
    os.chdir(dir)
    download_files_in_folder(folder_id)
    print("Download Complete\n")
    replaceConfig(folder_name)


def replaceConfig(folder_name):
    # Add yolov3 cfg to darknet_config cfg directory
    program_dir_path = os.getcwd()
    list = program_dir_path.split("/")
    index = list.index(folder_name)
    list = list[:index]
    program_dir_path = "/".join(list)
    download_gdrive_dir_name = "/" + str(folder_name) + "/"
    download_dir_path = program_dir_path + download_gdrive_dir_name
    rospack = rospkg.RosPack()
    darknet_config_path = rospack.get_path('darknet_config')
    os.chdir(darknet_config_path)
    os.chdir("./cfg")
    cfg_filename = "yolov3-tiny.cfg"
    for filename in os.listdir(download_dir_path):
        if "yolov3" in filename:
            cfg_filename = filename
    first_dir = download_dir_path + str(cfg_filename)
    second_dir = darknet_config_path + "/cfg/" + str(cfg_filename)
    if os.path.exists(cfg_filename):
        os.remove(cfg_filename)
        print(cfg_filename + " has been replaced in " + darknet_config_path + "/cfg/")
    else:
        print(cfg_filename + " has been added to " + darknet_config_path + "/cfg/")
    shutil.move(first_dir, second_dir)
    print()

    # CONSULTING THE CHART BOIII
    chartInput = raw_input("[1] Consult Chart, [any other char] Don't Consult Chart: ")
    print()
    os.chdir(download_dir_path)
    if chartInput == "1":
        os.system("xdg-open chart.png")

    # Moves content from backup to weight directory
    index = 0
    weightNames = []
    weight_filename = ""
    weight_choice = raw_input("[1] Select best.weights, [any other char] View Backup Directory: ")
    if weight_choice == "1":
        weight_filename = "yolov3-tiny_best.weights"
        for filename in os.listdir((download_dir_path + "weights/")):
            if "yolov3" in filename:
                weight_filename = filename
        first_dir = download_dir_path + "weights/" + weight_filename
        second_dir = darknet_config_path + "/weights/" + weight_filename
    else:
        print("***")
        for filename in os.listdir(download_dir_path + "weights/backup"):
            weightNames.append(filename)
            print("[" + str(index) + "] : " + str(filename))
            index += 1
        print("***")
        weightNamesIndex = raw_input("Choose Weight File: ")
        filename = weightNames[int(weightNamesIndex)]
        print("You have selected: " + filename)
        first_dir = download_dir_path + "weights/backup/" + str(filename)
        second_dir = darknet_config_path + "/weights/" + str(filename)
        weight_filename = filename
    os.chdir(darknet_config_path + "/weights/")
    if os.path.exists(weight_filename):
        os.remove(weight_filename)
        print(weight_filename + " has been replaced in " + darknet_config_path + "/weights/")
    else:
        print(weight_filename + " has been added to " + darknet_config_path + "/weights/")
    shutil.move(first_dir, second_dir)


    # Modify YAML file to change names and weight file chosen
    os.chdir(download_dir_path)
    with open('class_names.txt') as file1:
        yaml_names_arr = file1.readlines()
        yaml_names_arr = [line.rstrip('\n') for line in open('class_names.txt')]
    yolov3_tiny = {'yolo_model': {'threshold': {'value': 0.3}, 'detection_classes': {'names': yaml_names_arr}, 'weight_file': {'name': weight_filename}, 'config_file': {'name': cfg_filename}}}
    os.chdir(darknet_config_path)
    os.chdir("./yaml")
    yaml_file_name = "yolov3-tiny.yaml"
    os.remove(yaml_file_name)
    with open(yaml_file_name, "w") as file2:
        yaml.dump(yolov3_tiny, file2, default_flow_style=False)

searchAndDownloadWeight()
# replaceConfig("darknet_training_07-04-2019")
