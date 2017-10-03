# -*- coding: utf-8 -*-

# Python script for automated PhotoScan processing
# PhotoScan version 1.0.4
# Структура:
# +---01_Исходные_данные
# |   +---20131111
# |   |   |   GPS_20131111_1_20mm.txt
# |   |   |   GPS_20131111_1_35mm.txt
# |   |   |   TLM_20131111_1_20mm.txt
# |   |   |
# |   |   +---20131111_1_20mm
# |   |   |       20131111_1_20mm_0000.JPG
# |   |   |       20131111_1_20mm_0001.JPG
# |   |   |
# |   |   +---20131111_1_35mm
# |   |   \---20131111_2_20mm
# |   +---20141224
# |   \---20150615
# +---02_Проекты_Photoscan
# |       20131111.psz
# |
# +---03_Ортофотопланы
# |   \---20131111
# \---04_Dem
#Алгоритм:
#1. Проверить структуру вложенных папок
#2. Определить сколько папок с фотками
#3.

import os
import glob
# import PhotoScan
import math
import csv
import sys
import time
import shutil

# time.sleep(10800)
# DEFINE REPORT FILE
ReportFileName = "Report.xls"

# DEFINE DEFAULT REPORT ROW
ReportRow = ['Date','ChunkLabel','NumberPhotos','GPS','TLM','CamAligned','Optimization','DenseCloud','Model']

# DEFINE PROCESSING SETTINGS
print("---Defining processing settings...")

# Define: Coordinate System
CoordinateSystem_WGS = "EPSG::4326"

# Define; Coordinate System for current GAZPROM TRANSGAZ
CoordinateSystem_GT = "EPSG::32637"

# Define: Root folder for server
root_fld = u"V:\Photoscan_Cluster"

# Define: Home directory for eath harddisk with initial data
HomeDirectory = r'v:\Photoscan_Cluster\AirPatrol\GTMakhachkala\disk8'

HomeDirectory_out = r'v:\Photoscan_Cluster\AirPatrol\GTNNovgorod\finko_nn_22'

# Define: Source images Dir
AerialImagesDir = "01_Initial_data"

# Define: PhotoScan Project Dir
PhotoScanProjectFileDir = "02_Projects_Photoscan"

# Define: Source images Dir
OthoimagesDir = "03_Ortho"

# Define: DSMResolutions (in meters),
# 0 == GSD resolution
DSMResolutions = 0.1

# Define: OrthoImageResolutions (in meters)
# 0 == GSD resolution
OrthoImageResolutions = [1.00, 0]

# Define: AlignPhotosAccuracy ["HighestAccuracy", "HighAccuracy",
# "MediumAccuracy", "LowAccuracy", "LowestAccuracy"]
AlignPhotosAccuracy = "LowAccuracy"
AlignPhotosAccuracy1 = "MediumAccuracy"

# Define: AlignPointLimit - integer
AlignPointLimit = 8000
AlignPointLimit1 = 16000

# Define: AlignTiePointLimit - integer
AlignTiepointLimit = 2000
AlignTiepointLimit1 = 8000
# Define: BuildDenseCloudQuality ["lowest", "low", "medium", "high", "ultra"]
BuildDenseCloudQuality = "high"
# Define: BuildDenseCloudFilter ["mild", "moderate", "aggressive"]
BuildDenseCloudFilter = "moderate"

# Define: BuildGeometryQuality ["lowest", "low", "medium", "high", "ultra"]
BuildGeometryQuality = "medium"

# Define: BuildGeometryFaces [’low’, ‘medium’, ‘high’] or exact number.
BuildGeometryFaces = "medium"
# Threshold for PhotoScan error
ThresholdTottalError = int(20)
# Empty batches list for this folder
batch_list = []

def ReplaceComasToDots():
	path1 = os.path.dirname(os.path.join(HomeDirectory, AerialImagesDir))
	print("\n Идет замена в txt...")
	# console.flush()
	for dir in os.walk(path1):
		for txt_file in dir[2]:
			if txt_file[-3:]=='txt':
				os.chdir(dir[0])
				with open(os.path.join(txt_file), 'r') as txt1:
					filedata = txt1.read()
				filedata = filedata.replace(',', '.')
				with open(os.path.join(txt_file), 'w') as txt1:
					txt1.write(filedata)
	print("\n Идет замена в txt... Готово !")
	# console.flush()

def RenamePhotosNamesInTXT():
	path1 = os.path.dirname(os.path.join(HomeDirectory, AerialImagesDir))
	print("Идет замена в txt...")
	for dir in os.walk(path1):
		for txt_file in dir[2]:
			if txt_file[-3:]=='txt':
				if '20mm' in txt_file:
					os.chdir(dir[0])
					with open(os.path.join(txt_file), 'r') as txt1:
						filedata = txt1.read()
					filedata = filedata.replace('DSC', '20mm_')
					with open(os.path.join(txt_file), 'w') as txt1:
						txt1.write(filedata)
				if '' in txt_file:
					os.chdir(dir[0])
					with open(os.path.join(txt_file), 'r') as txt1:
						filedata = txt1.read()
					filedata = filedata.replace('DSC', '50mm_')
					with open(os.path.join(txt_file), 'w') as txt1:
						txt1.write(filedata)
				if '20mm' in txt_file:
					os.chdir(dir[0])
					with open(os.path.join(txt_file), 'r') as txt1:
						filedata = txt1.read()
					filedata = filedata.replace(',', '.')
					with open(os.path.join(txt_file), 'w') as txt1:
						txt1.write(filedata)
				if '50mm' in txt_file:
					os.chdir(dir[0])
					with open(os.path.join(txt_file), 'r') as txt1:
						filedata = txt1.read()
					filedata = filedata.replace(',', '.')
					with open(os.path.join(txt_file), 'w') as txt1:
						txt1.write(filedata)
	print("Идет замена в txt... Готово !")

def MoveReferenceFilesUpgrade():
	os.chdir(HomeDirectory)
	print("Home directory: " + HomeDirectory )
	path_init = os.path.join(HomeDirectory, AerialImagesDir)

	for d, dirs, files in os.walk(path_init):
		for txt_tlm in files:
			if txt_tlm[-3:] == 'txt':
				old_path = os.path.join(d, txt_tlm)
				print('old_path = ', old_path)
				new_path = os.path.join(d, '..','..', os.path.basename(txt_tlm))
				print('new_path = ', new_path)
				try:
					os.rename(old_path, new_path)
					shutil.move(old_path, new_path)
				except:
					pass

def MoveReferenceFiles():
	os.chdir(HomeDirectory)
	print("Home directory: " + HomeDirectory )
	path_init = os.path.join(HomeDirectory, AerialImagesDir)

	for d, dirs, files in os.walk(path_init):
		for txt_tlm in files:
			if txt_tlm[-3:] == 'txt':
				old_path = os.path.join(d, txt_tlm)
				print('old_path = ', old_path)
				new_path = os.path.join(d, '..', os.path.basename(txt_tlm))
				print('new_path = ', new_path)
				try:
					os.rename(old_path, new_path)
					shutil.move(old_path, new_path)
				except:
					pass

def RenamePhotoNames():
	print("Идет замена имен фотографий...")
	path2 = os.path.dirname(os.path.join(HomeDirectory, AerialImagesDir))
	pathiter = (os.path.join(root, filename)
		for root, k, filenames in os.walk(path2)
		for filename in filenames
	)
	for path in pathiter:
		if '20mm' in path:
			newname20 = path.replace('DSC', '20mm_')
			if newname20 != path:
				os.rename(path,newname20)
		if '50mm' in path:
			newname50 = path.replace('DSC', '50mm_')
			if newname50 != path:
				os.rename(path,newname50)
	print("Идет замена имен фотографий... Готово !")

def ConvertTXTtoCSV():
	headers = [1,10,12,13]
	print("Идет конвертация csv в txt...")
	path3 = os.path.dirname(os.path.join(HomeDirectory, AerialImagesDir))

	for dir in os.walk(path3):
		for txt_file in dir[2]:
			if txt_file[-3:]=='txt':
				csv_file = os.path.join(os.path.dirname(txt_file),os.path.basename(txt_file)[:-4]+'_TLM.csv')
				os.chdir(dir[0])
				#in_txt = csv.DictReader(open(txt_file,"rb"), delimiter = '\t')
				with open(txt_file, 'r') as in_txt, open(csv_file, 'w') as out_csv:
					reader = csv.DictReader(in_txt, fieldnames=[1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18], delimiter = '\t')
					writer = csv.DictWriter(out_csv, headers, extrasaction='ignore', delimiter = '\t')
					try:
						writer.writeheader()
						for line in reader:
							writer.writerow(line)
					except:
						pass
	print("Идет конвертация csv в txt... Готово !")

def CopyOnly20mm():
	os.chdir(HomeDirectory)
	print("Home directory: " + HomeDirectory )
	path_init = os.path.join(HomeDirectory, AerialImagesDir)
	print(path_init)
	path_out = os.path.join(HomeDirectory_out, AerialImagesDir)
	for d, dirs, files in os.walk(path_init):
		for file in files:
			if '20mm' in os.path.join(d, file):
				old_path = os.path.join(d, file)
				old_path_tree = os.path.dirname(old_path)
				print('old_path = ', old_path)
				new_path_tree = os.path.dirname(os.path.join(path_out, os.path.relpath(old_path, '01_Initial_data')))
				new_path = os.path.join(path_out, os.path.relpath(old_path, '01_Initial_data'))
				print('new_path = ', new_path)
				# try:
				os.makedirs(new_path_tree,  exist_ok=True)
				os.system('copy ' + old_path + ' ' + new_path)
#

# MoveReferenceFilesUpgrade()
# MoveReferenceFiles()
ReplaceComasToDots()
# RenamePhotosNamesInTXT()
# RenamePhotoNames()
ConvertTXTtoCSV()
# CopyOnly20mm()
