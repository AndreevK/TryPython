# -*- coding: utf-8 -*-

# Python script for automated PhotoScan processing
# PhotoScan version 1.2.5

import os
import glob
import PhotoScan
import math
import csv
import sys
import time
import gc
import imp 
from PySide import QtCore, QtGui
import collections
import numpy

class PipelineOrthoDlg(QtGui.QDialog):

	def __init__(self, parent):

		QtGui.QDialog.__init__(self, parent)

		self.setWindowTitle("Full pipeline ortho network proccesing")

		self.btnP1 = QtGui.QPushButton("Start")
		self.btnP1.setFixedSize(130,50)

		self.btnP2 = QtGui.QPushButton("Create batches")
		self.btnP2.setFixedSize(150,50)

		self.accuracy = QtGui.QLabel()
		self.accuracy.setText("Alignment accuracy :")
		self.accuracy.setFixedSize(130, 25)			

		self.accuracy_types = {"Lowest": PhotoScan.LowestAccuracy, "Low": PhotoScan.LowAccuracy, "Medium": PhotoScan.MediumAccuracy, "High": PhotoScan.HighAccuracy, "Highest": PhotoScan.HighestAccuracy }
		self.accuracy_types_sort = collections.OrderedDict(sorted(self.accuracy_types.items()))

		self.accuracyCmb = QtGui.QComboBox()  
		self.accuracyCmb.setFixedSize(100, 25)
		for type in self.accuracy_types_sort.keys():
			self.accuracyCmb.addItem(type)

		self.accuracy2 = QtGui.QLabel()
		self.accuracy2.setText("Alignment accuracy repeatedly :")
		self.accuracy2.setFixedSize(160, 25)			

		self.accuracy_types2 = {"Lowest": PhotoScan.LowestAccuracy, "Low": PhotoScan.LowAccuracy, "Medium": PhotoScan.MediumAccuracy, "High": PhotoScan.HighAccuracy, "Highest": PhotoScan.HighestAccuracy }
		collections.OrderedDict(sorted(self.accuracy_types2.items()))

		self.accuracyCmb2 = QtGui.QComboBox()  
		self.accuracyCmb2.setFixedSize(100, 25)
		for type in self.accuracy_types2.keys():
			self.accuracyCmb2.addItem(type)

		self.coorsys = QtGui.QLabel()
		self.coorsys.setText("Coordinate system:")
		self.coorsys.setFixedSize(160, 25)			

		self.coorsys_types = {"ГТ_Москва": 32637, "ГТ_Нижний_Новгород": 32638, "ГТ_Санкт-Петербург": 32636, "ГТ_Махачкала": 32638, "ГТ_Ставрополь": 32638, "ГТ_Саратов": 32638, "ГТ_Сургут": 32643, "ГТ_Уфа": 32640, "ГТ_Екатеринбург": 32641, "ГТ_Ставрополь": 32638, "ГТ_Казань": 32639, "ГТ_Краснодар": 32637, "ГТ_Самара": 32639, "ГТ_Ухта": 32638, "ГТ_Югорск": 32642, "ГТ_Волгоград": 32638, "Газпром_переработка": 32643 }
		collections.OrderedDict(sorted(self.coorsys_types.items()))

		self.coorsysCmb = QtGui.QComboBox()  
		self.coorsysCmb.setFixedSize(150, 25)
		for type in self.coorsys_types.keys():
			self.coorsysCmb.addItem(type)

		self.name = QtGui.QLabel()
		self.name.setText("Photoname:")
		self.name.setFixedSize(100, 25)			

		self.name_types = {"1": 1, "2": 2, "3": 3, "4": 4, "5": 5, "6": 6, "7": 7, "8": 8, "9": 9, "10": 10, "11": 11, "12": 12, "13": 13,"14": 14, "15": 15 }
		name_types_sort = collections.OrderedDict(sorted(self.name_types.items()))

		self.nameCmb = QtGui.QComboBox()  
		self.nameCmb.setFixedSize(150, 25)
		for type in self.name_types.keys():
			self.nameCmb.addItem(type)

		self.x = QtGui.QLabel()
		self.x.setText("Coordinate X:")
		self.x.setFixedSize(100, 25)			

		self.x_types = {"1": 1, "2": 2, "3": 3, "4": 4, "5": 5, "6": 6, "7": 7, "8": 8, "9": 9, "10": 10, "11": 11, "12": 12, "13": 13,"14": 14, "15": 15 }
		x_types_sort = collections.OrderedDict(sorted(self.x_types.items()))

		self.xCmb = QtGui.QComboBox()  
		self.xCmb.setFixedSize(150, 25)
		for type in self.x_types.keys():
			self.xCmb.addItem(type)

		self.y = QtGui.QLabel()
		self.y.setText("Coordinate Y:")
		self.y.setFixedSize(100, 25)			

		self.y_types = {"1": 1, "2": 2, "3": 3, "4": 4, "5": 5, "6": 6, "7": 7, "8": 8, "9": 9, "10": 10, "11": 11, "12": 12, "13": 13,"14": 14, "15": 15 }
		collections.OrderedDict(sorted(self.y_types.items()))

		self.yCmb = QtGui.QComboBox()  
		self.yCmb.setFixedSize(150, 25)
		for type in self.y_types.keys():
			self.yCmb.addItem(type)

		self.z = QtGui.QLabel()
		self.z.setText("Coordinate Z:")
		self.z.setFixedSize(100, 25)			

		self.z_types = {"1": 1, "2": 2, "3": 3, "4": 4, "5": 5, "6": 6, "7": 7, "8": 8, "9": 9, "10": 10, "11": 11, "12": 12, "13": 13,"14": 14, "15": 15 }
		collections.OrderedDict(sorted(self.z_types.items()))

		self.zCmb = QtGui.QComboBox()  
		self.zCmb.setFixedSize(150, 25)
		for type in self.z_types.keys():
			self.zCmb.addItem(type)

		self.PointLim = QtGui.QLabel()
		self.PointLim.setText("Points limit :")
		self.PointLim.setFixedSize(130, 25)			

		self.PointLimEdt = QtGui.QLineEdit()
		self.PointLimEdt.setPlaceholderText("limit of points")
		self.PointLimEdt.setFixedSize(100, 25)

		self.TiePointLim = QtGui.QLabel()
		self.TiePointLim.setText("Tie points limit :")
		self.TiePointLim.setFixedSize(130, 25)			

		self.TiePointLimEdt = QtGui.QLineEdit()
		self.TiePointLimEdt.setPlaceholderText("limit of tie points")
		self.TiePointLimEdt.setFixedSize(100, 25)

		self.Orthoq = QtGui.QLabel()
		self.Orthoq.setText("Ortho quality :")
		self.Orthoq.setFixedSize(130, 25)

		self.OrthoqEdt = QtGui.QLineEdit()
		self.OrthoqEdt.setPlaceholderText("e.g. 0.1")
		self.OrthoqEdt.setFixedSize(100, 25)			

		self.Trashold = QtGui.QLabel()
		self.Trashold.setText("Trashold error :")
		self.Trashold.setFixedSize(130, 25)			

		self.TrasholdEdt = QtGui.QLineEdit()
		self.TrasholdEdt.setPlaceholderText("e.g. 30")
		self.TrasholdEdt.setFixedSize(100, 25)

		self.NoAlingCams = QtGui.QLabel()
		self.NoAlingCams.setText("Trashold alinged cameras :")
		self.NoAlingCams.setFixedSize(130, 25)			

		self.NoAlingCamsEdt = QtGui.QLineEdit()
		self.NoAlingCamsEdt.setPlaceholderText("e.g. 150")
		self.NoAlingCamsEdt.setFixedSize(100, 25)

		self.pathToDisk = QtGui.QLabel()
		self.pathToDisk.setText("Path to initial data :")
		self.pathToDisk.setFixedSize(130, 25)			

		self.pathToDiskEdt = QtGui.QLineEdit()
		self.pathToDiskEdt.setPlaceholderText("full path")
		self.pathToDiskEdt.setFixedSize(100, 25)

		self.sleepEdt = QtGui.QLineEdit()
		self.sleepEdt.setPlaceholderText("e.g. 28800")
		self.sleepEdt.setFixedSize(100, 25)

		self.BatchValue = QtGui.QLabel()
		self.BatchValue.setText("Batches value :")
		self.pathToDisk.setFixedSize(100, 25)			

		self.BatchValueEdt = QtGui.QLineEdit()
		self.BatchValueEdt.setPlaceholderText("e.g. 10")
		self.BatchValueEdt.setFixedSize(100, 25)

		self.chkBox1 = QtGui.QCheckBox("Move reference files")
		self.chkBox1.setFixedSize(130,50)
		self.chkBox1.setToolTip("Перенести файлы телеметрии на уровень выше")
		
		self.chkBox2 = QtGui.QCheckBox("Replace comas")
		self.chkBox2.setFixedSize(130,50)
		self.chkBox2.setToolTip("Заменить в телеметрии запятые на точки")
		
		self.chkBox3 = QtGui.QCheckBox("Rename photos in .txt")
		self.chkBox3.setFixedSize(130,50)
		self.chkBox3.setToolTip("Заменить в телеметрии название фото с DSC на 20mm_ и 50mm_")

		self.chkBox4 = QtGui.QCheckBox("Rename photos")
		self.chkBox4.setFixedSize(130,50)
		self.chkBox4.setToolTip("Заменить название фото с DSC на 20mm_ и 50mm_")

		self.chkBox5 = QtGui.QCheckBox("Convert .txt to .csv")
		self.chkBox5.setFixedSize(130,50)
		self.chkBox5.setToolTip("Конвертировать .txt в .csv с параметрами z - 10 столбец, y - 12, x - 13")

		self.chkBox6 = QtGui.QCheckBox("Set timeout")
		self.chkBox6.setFixedSize(130,50)
		self.chkBox6.setToolTip("Установить таймаут на 8 часов перед началом обработки ")

		self.chkBox7 = QtGui.QCheckBox("Use only one lens")
		self.chkBox7.setFixedSize(130,50)
		self.chkBox7.setToolTip("Использовать только один объектив (в названии папки должно быть '_50')")

		layout = QtGui.QGridLayout()   #creating layout
		layout.addWidget(self.accuracy, 0, 2)
		layout.addWidget(self.accuracyCmb, 0, 3)
		layout.addWidget(self.accuracy2, 1, 2)
		layout.addWidget(self.accuracyCmb2, 1, 3)
		layout.addWidget(self.coorsys, 2, 2)
		layout.addWidget(self.coorsysCmb, 2, 3)
		layout.addWidget(self.x, 6, 2)
		layout.addWidget(self.xCmb, 6, 3)
		layout.addWidget(self.y, 7, 2)
		layout.addWidget(self.yCmb, 7, 3)
		layout.addWidget(self.z, 8, 2)
		layout.addWidget(self.zCmb, 8, 3)
		layout.addWidget(self.name, 9, 2)
		layout.addWidget(self.nameCmb, 9, 3)
		layout.addWidget(self.Orthoq, 5, 2)
		layout.addWidget(self.OrthoqEdt, 5, 3)
		layout.addWidget(self.PointLim, 0, 0)
		layout.addWidget(self.PointLimEdt, 0, 1)
		layout.addWidget(self.TiePointLim, 1, 0)
		layout.addWidget(self.TiePointLimEdt, 1, 1)
		layout.addWidget(self.pathToDisk, 2, 0)
		layout.addWidget(self.pathToDiskEdt, 2, 1)
		layout.addWidget(self.Trashold, 3, 2)
		layout.addWidget(self.TrasholdEdt, 3, 3)
		layout.addWidget(self.NoAlingCams, 4, 2)
		layout.addWidget(self.NoAlingCamsEdt, 4, 3)
		layout.addWidget(self.BatchValue, 10, 2)
		layout.addWidget(self.BatchValueEdt, 10, 3)
		layout.addWidget(self.chkBox6, 3, 0)
		layout.addWidget(self.sleepEdt, 3, 1)
		layout.addWidget(self.chkBox1, 4, 0)
		layout.addWidget(self.chkBox2, 5, 0)
		layout.addWidget(self.chkBox3, 6, 0)
		layout.addWidget(self.chkBox4, 7, 0)
		layout.addWidget(self.chkBox5, 8, 0)
		layout.addWidget(self.chkBox7, 9, 0)
		layout.addWidget(self.btnP1, 11, 3)
		layout.addWidget(self.btnP2, 11, 2)

		self.setLayout(layout)  

		QtCore.QObject.connect(self.btnP1, QtCore.SIGNAL("clicked()"), self.PipelineProcess)
		QtCore.QObject.connect(self.btnP2, QtCore.SIGNAL("clicked()"), self.MapTailerBatch)
		
		# self.exec()

	
 
# ------------------------------------------------------------------------------------------------------------------------------------------------
	def PipelineProcess(self):

		def ReplaceComasToDots():
			path1 = os.path.dirname(os.path.join(HomeDirectory, AerialImagesDir))
			console.write("\n Идет замена в txt...")
			console.flush()
			for dir in os.walk(path1):
				for txt_file in dir[2]:
					if txt_file[-3:]=='txt':
						os.chdir(dir[0])
						with open(os.path.join(txt_file), 'r') as txt1:
							filedata = txt1.read()
						filedata = filedata.replace(',', '.')
						with open(os.path.join(txt_file), 'w') as txt1:
							txt1.write(filedata)
			console.write("\n Идет замена в txt... Готово !")
			console.flush()

		def MoveReferenceFiles():
			os.chdir(HomeDirectory)
			console.write("\n Home directory: " + HomeDirectory )
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
		# замена в *.txt
		def RenamePhotosNamesInTXT():
			path1 = os.path.dirname(os.path.join(HomeDirectory, AerialImagesDir))
			console.write("\n Идет замена в txt...")
			console.flush()
			for dir in os.walk(path1):
				for txt_file in dir[2]:
					if txt_file[-3:]=='txt':
						if '25mm' in txt_file:
							os.chdir(dir[0])
							with open(os.path.join(txt_file), 'r') as txt1:
								filedata = txt1.read()
							filedata = filedata.replace('DSC', '25mm_')
							with open(os.path.join(txt_file), 'w') as txt1:
								txt1.write(filedata)
						if '50mm' in txt_file:
							os.chdir(dir[0])
							with open(os.path.join(txt_file), 'r') as txt1:
								filedata = txt1.read()
							filedata = filedata.replace('DSC', '50mm_')
							with open(os.path.join(txt_file), 'w') as txt1:
								txt1.write(filedata)
						if '25mm' in txt_file:
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
						if '20mm' in txt_file:
							os.chdir(dir[0])
							with open(os.path.join(txt_file), 'r') as txt1:
								filedata = txt1.read()
							filedata = filedata.replace('DSC', '20mm_')
							with open(os.path.join(txt_file), 'w') as txt1:
								txt1.write(filedata)
						if '20mm' in txt_file:
							os.chdir(dir[0])
							with open(os.path.join(txt_file), 'r') as txt1:
								filedata = txt1.read()
							filedata = filedata.replace(',', '.')
							with open(os.path.join(txt_file), 'w') as txt1:
								txt1.write(filedata)
			console.write("\n Идет замена в txt... Готово !")
			console.flush()
		# Замена имени фотографий
		def RenamePhotoNames():
			console.write("\n Идет замена имен фотографий...")
			console.flush()
			path2 = os.path.dirname(os.path.join(HomeDirectory, AerialImagesDir))
			pathiter = (os.path.join(root, filename)
				for root, k, filenames in os.walk(path2)
				for filename in filenames
			)
			for path in pathiter:
				if '25mm' in path:
					newname20 = path.replace('DSC', '25mm_')
					if newname20 != path:
						os.rename(path,newname20)
				if '50mm' in path:
					newname50 = path.replace('DSC', '50mm_')
					if newname50 != path:
						os.rename(path,newname50)
				if '20mm' in path:
					newname20 = path.replace('DSC', '20mm_')
					if newname20 != path:
						os.rename(path,newname20)
			console.write("\n Идет замена имен фотографий... Готово !")
			console.flush()
		# конвертация *.txt  *.csv
		def ConvertTXTtoCSV():
			x = self.x_types[self.xCmb.currentText()]
			y = self.y_types[self.yCmb.currentText()]
			z = self.z_types[self.zCmb.currentText()]
			headers = [1,z,y,x]
			console.write("\n Идет конвертация csv в txt...")
			console.flush()
			path3 = os.path.dirname(os.path.join(HomeDirectory, AerialImagesDir))
			for dir in os.walk(path3):
				for txt_file in dir[2]:
					if txt_file[-3:]=='txt':
						csv_file = os.path.join(os.path.dirname(txt_file),os.path.basename(txt_file)[:-4]+'_TLM.csv')
						os.chdir(dir[0])
						#in_txt = csv.DictReader(open(txt_file,"rb"), delimiter = '\t')
						with open(txt_file, 'r') as in_txt, open(csv_file, 'w') as out_csv:
							reader = csv.DictReader(in_txt, fieldnames=[1,2,3,4,5,6,7,8,9,10,11,12,13,14,15], delimiter = '\t')
							writer = csv.DictWriter(out_csv, headers, extrasaction='ignore', delimiter = '\t')
							try:
								writer.writeheader()
								for line in reader:
									writer.writerow(line)
							except:
								pass
			console.write("\n Идет конвертация csv в txt... Готово !")
			console.flush()

		def getSubDir(pathDir): # List of subdirs in dir
			dirs = []
			listDir = os.listdir(pathDir)
			for d in listDir:
				if (os.path.isdir(os.path.join(pathDir,d))):
					dirs.append(d)
			if self.chkBox7.isChecked():	
				for d in dirs:
					if '_50mm' in d:
						dirs.remove(d)
					else:
						pass
			dirs.sort()
			return dirs

		def getOrientationFile(pathDir,fileName):
			listDir = os.listdir(pathDir)
			orientationFiles = []
			for d in listDir:
				if (fileName in d) and (os.path.isfile(os.path.join(pathDir,d))):
					orientationFiles.append(d)
			for i in orientationFiles:
				if ("GPS" in i):
					return i

			for i in orientationFiles:
				if ("TLM" in i):
					return i
			return ""

		def ReGetOrientationFile(pathDir,fileName):
			listDir = os.listdir(pathDir)
			orientationFiles = []
			for d in listDir:
				if (fileName in d) and (os.path.isfile(os.path.join(pathDir,d))):
					orientationFiles.append(d)
			for i in orientationFiles:
				if ("RBLD" in i):
					return i
			return ""

		def getListProjects(pathDir):
			listDir = os.listdir(pathDir)
			listProjects =[f for f in listDir if (".psx" in f) and (os.path.getsize(os.path.join(pathDir,f)) > 100)]
			listProjects.sort()
			return listProjects

		def isLock(prj):
			listDir = os.listdir(PhotoScanProjectFileDir)
			if  prj + ".lock" in listDir:
				return True
			return False

		def isLockNetwork(prj):
			listDir = os.listdir(PhotoScanProjectFileDir)
			if prj + ".lock" in listDir:
				return True
			return False

		def lockProject(prj):
			f = open(os.path.join(PhotoScanProjectFileDir,prj + ".lock"), 'w')
			f.close()
			return

		def unlockProject(prj):
			os.remove(os.path.join(root_fld, prj + ".lock"))
			return

		def mean(list):
			return float(sum(list)) / max(len(list), 1)

		def MatchAndAlignPhotos():

			accuracy = self.accuracy_types[self.accuracyCmb.currentText()]
			keypoint = float(self.PointLimEdt.text())
			tiepoint = float(self.TiePointLimEdt.text())

			task1 = PhotoScan.NetworkTask()
			task2 = PhotoScan.NetworkTask()

			console.write("\n Network procces for match photos")
			console.flush()

			task1.frames.append((chunk.key,0))
			task1.name = "MatchPhotos"
			task1.params['downscale'] = int(accuracy)
			task1.params['keypoint_limit'] = keypoint
			task1.params['tiepoint_limit'] = tiepoint
			task1.params['select_pairs'] = int(PhotoScan.ReferencePreselection)
			task1.params['network_distribute'] = True

			console.write("\n Network procces for aling photos")
			console.flush()

			task2.chunks.append(chunk.key)
			task2.name = "AlignCameras"
			task2.params['network_distribute'] = True

			return (task1, task2)

		def MatchAndAlignPhotos2():

			accuracy = self.accuracy_types2[self.accuracyCmb2.currentText()]
			keypoint = float(self.PointLimEdt.text()) * 2
			tiepoint = float(self.TiePointLimEdt.text()) *1.5

			task1 = PhotoScan.NetworkTask()
			task2 = PhotoScan.NetworkTask()

			console.write("\n Network procces for match photos")
			console.flush()

			task1.frames.append((chunk.key,0))
			task1.name = "MatchPhotos"
			task1.params['downscale'] = int(accuracy)
			task1.params['keypoint_limit'] = keypoint
			task1.params['tiepoint_limit'] = tiepoint
			task1.params['select_pairs'] = int(PhotoScan.ReferencePreselection)
			task1.params['network_distribute'] = True

			console.write("\n Network procces for aling photos")
			console.flush()

			task2.chunks.append(chunk.key)
			task2.name = "AlignCameras"
			task2.params['network_distribute'] = True

			return (task1, task2)


		def DemOrthoExport():

			epsg = str('EPSG::' + str(self.coorsys_types[self.coorsysCmb.currentText()]))
			orthoquality = float(self.OrthoqEdt.text())
			
			task3 = PhotoScan.NetworkTask()
			task4 = PhotoScan.NetworkTask()
			task5 = PhotoScan.NetworkTask()

			console.write("\n ---Network procces for building DEM")
			console.flush()

			task3.frames.append((chunk.key,0))
			task3.name = "BuildDem"
			task3.params['source_data'] = 0
			task3.params['projection'] = epsg
			task3.params['network_distribute'] = True

			console.write("\n ---Network procces for building ortho")
			console.flush()

			task4.frames.append((chunk.key,0))
			task4.name = "BuildOrthomosaic"
			task4.params['ortho_surface'] = 0
			task4.params['resolution_x'] = orthoquality
			task4.params['resolution_y'] = orthoquality
			task4.params['network_distribute'] = True

			console.write("\n ---Network procces for exporting ortho")
			console.flush()

			task5.frames.append((chunk.key,0))
			task5.name = "ExportOrthomosaic"
			task5.params['write_world'] = 1
			task5.params['tile_width'] = 8192
			task5.params['write_tiles'] = 1
			task5.params['path'] = pathortho
			task5.params['resolution_x'] = orthoquality
			task5.params['resolution_y'] = orthoquality
			task5.params['tile_height'] = 8192
			task5.params['raster_format'] = 2
			task5.params['projection'] = epsg

			return (task3, task4, task5)

		def CalculateTotalError():
			threshold = float(self.TrasholdEdt.text())
			err_list = []
			crt_err_list = []
			for camera in chunk.cameras:
				if camera.transform:
					try:
						#source values in geographic coordinate system
						sourceGeogr = camera.reference.location 
						#estimated position in geographic coordinate system
						estGeogr = chunk.crs.project(chunk.transform.matrix.mulp(camera.center))
						#measured values in geocentric coordinates
						sourceGeoc = chunk.crs.unproject(camera.reference.location)
						#estimated coordinates in geocentric coordinates
						estimGeoc = chunk.transform.matrix.mulp(camera.center) 
						#local LSE coordinates
						local = chunk.crs.localframe(chunk.transform.matrix.mulp(camera.center))
						# vector error
						error_vec = local.mulv(estimGeoc - sourceGeoc)
						# norm error
						error_norm = error_vec.norm()
						err_list.append(error_norm)

						if float(error_norm) > int(25):
							crt_err_list.append(camera)
						else:
							pass
					except:
						pass
				else:
					continue

			total_err =  mean(err_list)

			console.write("\n ---Total geographic error for : " + str(batch) + " : --- " + str(total_err))
			console.flush()

			# if len(crt_err_list) > int(100):
			# 	critical_err_value = len(crt_err_list)
			# 	return critical_err_value
			# else:
			# 	pass

			if float(total_err) > threshold:
				return True

		def CompateAlignedAndNotAlignedCameras():

			for p in cameras:
				if p.transform:
					align_cameras.append(p)
				else:
					pass

			camer_set = set(cameras)
			align_cameras_set = set(align_cameras)
			diff = camer_set - align_cameras_set	

			return diff

		def BoostRegionSize():

			region = chunk.region
			region.size = region.size * 5
			chunk.region = region
			console.write("\n ---Region successfully boosted")
			console.flush()

		# Define: Coordinate System
		CoordinateSystem_WGS = "EPSG::4326"

		# Define: Root folder for server
		root_fld = "V:\Photoscan_Cluster"

		# Define: server adress
		server_ip = '192.168.254.50'

		# Define: Source images Dir
		AerialImagesDir = "01_Initial_data"

		# Define: PhotoScan Project Dir
		PhotoScanProjectFileDir = "02_Projects_Photoscan"

		# Define: Source images Dir
		OthoimagesDir = "03_Ortho"

		# Empty batches list for this folder
		batch_list = set()


		# Define: Home directory for eath harddisk with initial data
		HomeDirectory = str(self.pathToDiskEdt.text())

		# Define: 
		path_rep_file = os.path.join(HomeDirectory, 'Processing_report.txt')

		client = PhotoScan.NetworkClient()
		chunk = doc.chunk

		console = open(path_rep_file, 'w+')
		console.write("\n ---Run script...")
		console.flush()

		# Set home folder
		os.chdir(HomeDirectory)
		# console.write("\n Home directory: " + HomeDirectory )
		# console.flush()

	
		doc.clear()

		if self.chkBox6.isChecked():
			time.sleep(int(self.PointLimEdt.text()))
		if self.chkBox1.isChecked():
			MoveReferenceFiles()
		if self.chkBox2.isChecked():
			ReplaceComasToDots()
		if self.chkBox3.isChecked():
			RenamePhotosNamesInTXT()
		if self.chkBox4.isChecked():
			RenamePhotoNames()
		if self.chkBox5.isChecked():
			ConvertTXTtoCSV() 


		os.chdir(HomeDirectory)
		console.write("\n Home directory: " + HomeDirectory )
		console.flush()
		# Build dirs structure
		if not(os.path.exists(AerialImagesDir)):
			os.mkdir(AerialImagesDir)
		if not(os.path.exists(PhotoScanProjectFileDir)):
			os.mkdir(PhotoScanProjectFileDir)
		if not(os.path.exists(OthoimagesDir)):
			os.mkdir(OthoimagesDir)

		listDirPhoto = getSubDir(AerialImagesDir)# Столько будет проектов, название проекта брать отсюда
		console.write("\n ---Directories of Flys: " + ','.join(listDirPhoto))
		console.flush()

		listNonExistsProjects = [prj for prj in listDirPhoto if not(os.path.exists(os.path.join(PhotoScanProjectFileDir,prj + "_1" + ".psx")))]
		console.write("\n ---Not founded projects: "+ ','.join(listNonExistsProjects))
		console.flush()
		# Здесь будет большой цикл, для каждого проекта из списка выполнять
		if len(listNonExistsProjects) != 0:
			for dd in listNonExistsProjects:
				activeProjectDirDate = os.path.join(AerialImagesDir,dd)
				listDirs = getSubDir(activeProjectDirDate) # Список директорий с фотками
				listDirs = [dr for dr in listDirs if not("Dist" in listDirs)]
				 # Для каждой в списке:
								   # 1. создать чанк если в ней есть фотки
								   # 2. Загрузить фотки
								   # 3. Загрузить координаты
								   # 4. Сохранить проект
				for activeDirPhoto in listDirs:
					listPhotos = []
					if glob.glob(os.path.join(activeProjectDirDate,activeDirPhoto,"*.JPG")):
						listPhotos = glob.glob(os.path.join(activeProjectDirDate,activeDirPhoto,"*.JPG"))

						# create chunk

						console.write("\n ---Create chunk : " + activeDirPhoto)
						console.flush()
						chunk = doc.addChunk()
						doc.chunk
						chunk.label = activeDirPhoto

						# dictRow['ChunkLabel'] = chunk.label

						# LOAD AERIAL IMAGES

						console.write("\n ---Loading images...")
						console.flush()
				
						chunk.addPhotos(listPhotos)
						camera = chunk.cameras[0]


						# LOAD CAMERA ORIENTATIONS

						try: # Изза бага в функции chunk.cameras.add пришлось так сделать
							console.write("\n ---Loading initial photo orientations...")
							console.flush()
						except:
							console.write("\n ")
							console.flush()
						orientationFile = getOrientationFile(activeProjectDirDate,activeDirPhoto)
						# if ("GPS" in orientationFile):
						# 	dictRow['GPS'] = "1"
						# 	CoordinateSystemEPSG = CoordinateSystemEPSG_GPS
						# else:
						# 	dictRow['TLM'] = "1"
						CoordinateSystemEPSG = CoordinateSystem_WGS
						

						# SET COORDINATE SYSTEM
						
						# init coordinate system object
						CoordinateSystem = PhotoScan.CoordinateSystem(CoordinateSystemEPSG)
						console.write("\n ---Settings coordinate system: " + str(CoordinateSystem))
						console.flush()
						if not(CoordinateSystem.init(CoordinateSystemEPSG)):
							app.messageBox("Coordinate system EPSG code not recognized!")
						# define coordinate system in chunk
						chunk.crs = CoordinateSystem

						#chunk.projection = CoordinateSystem

						console.write("\n Orientation File: " + orientationFile)
						console.flush()
						# Load chunk reference file
						chunk.loadReference(os.path.join(activeProjectDirDate,orientationFile),'csv', 'nzyx')
						
						# writer.writerow(dictRow)

				#SAVE PROJECT

				# Cycle for initial data with (---50mm--- and ---20mm---) lenses
				chl = doc.chunks
				if self.chkBox7.isChecked():
					if not len(doc.chunks) == 1:
						doc.mergeChunks(chl)
						for i in chl:
							doc.remove(i)
				else:
					if not len(doc.chunks) == 1:
						tmm = []
						fmm = []
						for i in chl:
							if '20mm' in i.label:
								tmm.append(i)
							else:
								fmm.append(i)
						for i in range(len(tmm)):
							for j in range(len(fmm)):
								if tmm[i].label == fmm[j].label.replace('50mm', '20mm'):
									doc.mergeChunks([tmm[i], fmm[j]])
						for i in chl:
							doc.remove(i)	

				for l, i in enumerate(doc.chunks):
					i.label = str(l+1)
					if not(doc.save(os.path.join(PhotoScanProjectFileDir,dd + "_" + i.label + ".psx"),[i])):
						app.messageBox("Saving project failed!")
				try:
					if chunk.loadReference(os.path.join(activeProjectDirDate,orientationFile),'csv', 'nzyx') == False:
						nameProject_inst = os.path.join(dd + "_" + i.label + ".psx")
						print(nameProject_inst)
						lockProject(nameProject_inst)
				except:
					pass


				console.write("\n ---Saving project... : " + str(dd))
				console.flush()

				#Clearing doc

				doc.clear()

		# #All init done! Ready to start processing.

		# #Cycle for match and aling photos in projects


		console.write("\n -----Start network processing...-----")
		console.flush()
		full_checked_prjs = set()
		listProjects = getListProjects(PhotoScanProjectFileDir)
		# console.write("\n ---Find projects: ", len(listProjects))
		# console.flush()
		for nameProject in listProjects:
			pathortho = os.path.join(HomeDirectory, OthoimagesDir,nameProject[:-4], nameProject[:-4] + '.jpg')
			#Condition for creating ortho folders
			if not(os.path.exists(os.path.join(HomeDirectory,OthoimagesDir,nameProject))):
				try:
					os.mkdir(os.path.join(HomeDirectory,OthoimagesDir,nameProject[:-4]))
				except:
					pass
			#Locking project 
			if isLock(nameProject) == True:
				pass
			else:
				console.write("\n ---Open project: " + nameProject)
				console.flush()
				pathOpenProject = os.path.join(PhotoScanProjectFileDir,nameProject)
				pathclient = os.path.join(HomeDirectory, pathOpenProject)
				prj_path = os.path.relpath(pathclient, root_fld)

				if not ".lock" in pathOpenProject:

					doc.open(pathOpenProject)
					lockProject(nameProject)
					chunk = doc.chunk
					chunks = doc.chunks
					frames = chunk.frames
					if chunk.point_cloud:

						BoostRegionSize()

						pathortho = os.path.join(HomeDirectory, OthoimagesDir, os.path.basename(prj_path[:-4]), os.path.basename(prj_path[:-4]) + '.jpg')
						tasks = DemOrthoExport()

						pathbatch = pathOpenProject
						client.connect(server_ip)
						batch_id = client.createBatch(prj_path, [tasks[0], tasks[1], tasks[2]])
						client.resumeBatch(batch_id)

						# batch_list.add(batch_id)
						full_checked_prjs.add(prj_path)

						doc.clear()

						console.write("\n ---Project aligned and preprering for export ortho... : " + prj_path)
						console.flush()
					
						console.flush()
					else:

						tasks =  MatchAndAlignPhotos()
						
						pathbatch = pathOpenProject
						client.connect(server_ip)
						batch_id = client.createBatch(prj_path, [tasks[0], tasks[1]])
						batch_status = client.batchStatus(batch_id)
						# console.write("\n ---batch_status", batch_status)
						client.resumeBatch(batch_id)
						console.write("\n ---Project preprering for aligning... : " + prj_path)
						console.flush()
						batch_list.add(batch_id)
						doc.clear()
						gc.collect()
						# batch_list_u = [i.encode('utf-8') for i in batch_list]
						# console.write("\n ---batch_list :", batch_list)

		console.write("\n ---Find projects in " + HomeDirectory + " proccesing on network: ---" + (str(batch_list)))
		console.flush()

		# Big cycle for network proccesing with points-proof and error checking

		client.connect(server_ip)

		batch_list_temp = batch_list
		while len(batch_list) != 0:
			# console.write("\n ===Beginning new cycle===")
			# console.flush()
			for batch in batch_list:
				batch_info = client.batchStatus(batch)
				if batch_info['status'] == 'completed':
					prj_path =  batch_info['path']
					console.write("\n ---Reopening project with align photos for check errors first time: " + str(batch))
					console.flush()
					doc.open(os.path.join(root_fld, prj_path))
					console.write("\n Path to opening --- : " + os.path.join(root_fld, prj_path))
					console.flush()
					chunk = doc.chunk
					frames = chunk.frames
					cameras = chunk.cameras
					align_cameras = []
					
					#check if error > threshold and need to rebuild TLM file
					total_error = CalculateTotalError()

					# if total_error == critical_err_value:

					if total_error == True:

						batch_list.remove(batch)
						full_checked_prjs.add(batch)
						unlockProject(prj_path)
						
						console.write("\n ---Total error too high, need manual checking...")
						console.flush()

						
						doc.clear()
						gc.collect()
						del chunk
						del frames
						del cameras
						del align_cameras
						del total_error
						del prj_path
						del batch_info

						break
											
					else: # If threshold is OK!
						# check number alinged photos ( not more then 150 not aligned photos)
						diff = CompateAlignedAndNotAlignedCameras()	
						trasholdcams = float(self.NoAlingCamsEdt.text())

						if len(diff) > trasholdcams:

							tasks = MatchAndAlignPhotos2()

							client.connect(server_ip)
							batch_id = client.createBatch(prj_path, [tasks[0], tasks[1]])
							# batch_status = client.batchStatus(batch_id)
							client.resumeBatch(batch_id)

							console.write("\n ---Problem project  *" + str(batch) +  "* successfully processed on network repeatedly with high accuracy")
							console.flush()

							batch_list.remove(batch)
							full_checked_prjs.add(batch_id)
							unlockProject(prj_path)

							doc.clear()
							gc.collect()
							del trasholdcams
							del diff 
							del batch_info
							del chunk
							del frames
							del cameras
							del align_cameras
							del total_error
							del tasks 
							del batch_id

							break		

						else:
							pathortho = os.path.join(HomeDirectory, OthoimagesDir, os.path.basename(batch_info['path'][:-4]), os.path.basename(batch_info['path'][:-4]) + '.jpg')
							console.write("\n ---Project number * " + str(batch) + " * successfully aligned and processed on network")
							console.flush()

							BoostRegionSize()

							tasks = DemOrthoExport()

							client.connect(server_ip)
							batch_id = client.createBatch(prj_path, [tasks[0], tasks[1], tasks[2]])
							client.resumeBatch(batch_id)

							batch_list.remove(batch)
							full_checked_prjs.add(batch)
							
							doc.clear()
							gc.collect()
							del diff 
							del batch_info
							del chunk
							del frames
							del cameras
							del align_cameras
							del total_error
							del tasks 
							del batch_id

							console.write("\n ---Project successfully aligned and preprering for export ortho... : " + str(batch))
							console.flush()

							break

				else:
					del batch_info
					doc.clear()
					gc.collect()

		print("---Initial batch list: " + str(batch_list_temp))
		print("---Final full checked projects :" + str(full_checked_prjs))			
		print("===Network proccesing completed===")


	def MapTailerBatch(self):

		def BatchChunks(l, n):
			for i in range(0, len(l), n):
				yield l[i:i + n]

		def CreateListAndBatch4Orthos(ortho_path):

			if os.path.isfile(os.path.join(HomeDirectory, ortho_path + '_list.txt')) == True:
				pass
			else:
				if os.path.isfile(os.path.join(HomeDirectory, ortho_path + '_batch.bat')) == True:
					pass
				else:
					# try:
					list_dir_ortho = os.listdir(ortho_path)
					jpgs = filter(lambda x: x.endswith('.jpg'), list_dir_ortho)
					del list_dir_ortho
					jpgs = [os.path.join(HomeDirectory, ortho_path, jpg) for jpg in jpgs]
					# try:
					with open(os.path.join(ortho_path,'..', os.path.basename(ortho_path) + '_list.txt'), 'w') as orthofile:
						orthofile.write('\n'.join(jpgs))
					with open(os.path.join(ortho_path,'..', os.path.basename(ortho_path) + '_batch.bat'), 'w') as batchfile:
						batchfile.write('"c:\Program Files\MapTiler Pro\maptiler.exe" -f jpeg -nodata 0 0 0 -zoom 9 19 -resampling near -store mbtiles -o C:\\' + os.path.basename(ortho_path) + '.mbtiles -srs EPSG:' + str(self.coorsys_types[self.coorsysCmb.currentText()]) + ' --optfile ' + os.path.join(HomeDirectory, ortho_path,'..', os.path.basename(ortho_path)) + '_list.txt')
					return True
					# 	except:
					# 		pass
					# except:
					# 	pass

		def CreateBatch4Batches():

			batch_value = int(self.BatchValueEdt.text())
			if os.path.isfile(os.path.join(HomeDirectory, OrthoimagesDir + 'BATCH_list.bat')) == True:
				pass
			else:
				try:
					list_dir_ortho = os.listdir(OrthoimagesDir)
					bats = filter(lambda x: x.endswith('.bat'), list_dir_ortho)
					del list_dir_ortho
					bats = [os.path.join(HomeDirectory, OrthoimagesDir, bat) for bat in bats]
					batch_chunks = list(BatchChunks(bats, batch_value))
					try:
						n = 0
						for i in batch_chunks:
							k = n+1
							with open(os.path.join(HomeDirectory, OrthoimagesDir, 'BATCH_list_' + str(k) + '.bat'), 'w') as batchfile:
								[batchfile.write('call "' + bat + '"\n') for bat in i]
							n = k
						return True
					except:
						pass
				except:
					pass
		# Define: Coordinate System
		CoordinateSystem_WGS = "EPSG::4326"

		# Define: Root folder for server
		root_fld = "V:\Photoscan_Cluster"

		# Define: server adress
		server_ip = '192.168.254.50'

		# Define: Source images Dir
		AerialImagesDir = "01_Initial_data"

		# Define: PhotoScan Project Dir
		PhotoScanProjectFileDir = "02_Projects_Photoscan"

		# Define: Source images Dir
		OrthoimagesDir = "03_Ortho"

		# Empty batches list for this folder
		batch_list = set()

		# Define: Home directory for eath harddisk with initial data
		HomeDirectory = str(self.pathToDiskEdt.text())

		# Define: 
		path_rep_file = os.path.join(HomeDirectory, 'Batch_report.txt')

		client = PhotoScan.NetworkClient()

		console = open(path_rep_file, 'w+')
		console.write("\n ---Run script...")
		console.flush()

		# Set home folder
		os.chdir(HomeDirectory)

		console.write("\n Home directory: " + HomeDirectory)
		console.flush()

		ortho_path = os.listdir(OrthoimagesDir) # F:\Andreev_K\pythonscan\pythonscan0.01\03_Ortho\20160110_1
		ortho_path = [os.path.join(OrthoimagesDir, ortho) for ortho in ortho_path]
		console.write("\n ---Ortho dirs : " + str(ortho_path))
		console.flush()
		for i in ortho_path:
			result = CreateListAndBatch4Orthos(i)
			if result:
				console.write("\n Creating list of files in orthodir " + str(i) + " successful")
				console.flush()
			else:
				console.write("\n Cannot create list of files in orthodir" + str(i))
				console.flush()
		
		result2 = CreateBatch4Batches()
		if result2:
			console.write("\n Creating batch of batches in orthodir successful")
			console.flush()
		else:
			console.write("\n Cannot create batch of batches in orthodir")
			console.flush()


def main():

		# get main app objects
	global doc
	doc = PhotoScan.app.document

	app = QtGui.QApplication.instance()
	parent = app.activeWindow()

	dlg = PipelineOrthoDlg(parent)
	dlg.exec()

	gc.enable()
	gc.DEBUG_LEAK

	

	

PhotoScan.app.addMenuItem("Custom/Full pipeline ortho network proccesing", main)
