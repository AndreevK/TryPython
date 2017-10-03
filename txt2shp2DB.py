import gdal
import os, subprocess
import csv
from gdal import ogr
import glob

# Choose your PostgreSQL version here
os.environ['PATH'] += r';C:\Program Files\PostgreSQL\9.5\bin'
os.environ['PGHOST'] = '192.168.254.50'
os.environ['PGPORT'] = '5432'
os.environ['PGUSER'] = 'postgres'
os.environ['PGPASSWORD'] = 'admin'
# -----------------------------------------------------ARGUMENT 1
os.environ['PGDATABASE'] = 'transgaz_moskva'
# -----------------------------------------------------ARGUMENT 2
dirname= r"finko_orto_062"
# -----------------------------------------------------ARGUMENT 3
# base_dir = r"T:\0000_AirPatrol\AirpPatrol_Report\Finko\GTMoscow\04"
base_dir = os.path.dirname(__file__)

def ReplaceComasToDots():
    for dir in os.walk(base_dir):
        for txt_file in dir[2]:
            if txt_file[-3:] == 'txt':
                    os.chdir(dir[0])
                    with open(os.path.join(txt_file), 'r') as txt1:
                        filedata = txt1.read()
                    filedata = filedata.replace(',', '.')
                    filedata = filedata.replace('		', '	')
                    with open(os.path.join(txt_file), 'w') as txt1:
                        txt1.write(filedata)

def ConvertTXTtoCSV():
    for dir in os.walk(base_dir):
        for txt_file in dir[2]:
             if txt_file[-3:]=='txt':
                 try:
                    csv_file = os.path.join(os.path.dirname(txt_file),os.path.basename(txt_file)[:-3]+'csv')
                    os.chdir(dir[0])
                    in_txt = csv.reader(open(txt_file,'r'), delimiter = '\t')
                    out_csv = csv.writer(open(csv_file, 'w'))
                    out_csv.writerows(in_txt)
                 except:
                    pass
                 print("---Successfully converted", txt_file, "to .csv")
def CreatingSHPfromCSV():

    for dir in os.walk(base_dir):
         for file_name in dir[2]:
             if file_name[-3:]=='csv':
                 lines = open(file_name).readlines()
                 open (file_name,'w').writelines(lines[4:])
                 os.chdir(dir[0])
                 fname=file_name[0:-4]
                 fvrt = open(fname+'.vrt', 'wt')
                 fvrt.write('<OGRVRTDataSource>\n'
                            '<OGRVRTLayer name="'+fname+'">\n'
                            '<SrcDataSource>'+fname+'.csv</SrcDataSource>\n'
                            '<GeometryType>wkbPoint</GeometryType>\n'
                            '<LayerSRS>WGS84</LayerSRS>\n'
                            '<GeometryField encoding="PointFromColumns" x="field_4" y="field_5"/>\n'
                            '</OGRVRTLayer>\n'
                            '</OGRVRTDataSource>\n')
                 fvrt.close()
                 os.system('ogr2ogr '+fname+'.shp '+fname+'.vrt')
                 os.system('del '+fname+'.vrt')
                 print("---Successfully created", file_name, "shapefile")

def AddColunmsToSHP():

    full_dir = os.walk(base_dir)
    shapefile_list = []
    for source, dirs, files in full_dir:
        for file_ in files:
            if file_[-3:] == 'shp':
                shapefile_path = os.path.join(source, file_)
                shapefile_list.append(shapefile_path)
                infile=gdal.OpenEx(shapefile_path, gdal.GA_Update)
                fieldDefn=ogr.FieldDefn('filename', ogr.OFTString)
                fieldDefn.SetWidth(254)
                inlyr=infile.GetLayer()
                # inlyr=inlyr.GetLayerDefn()
                inlyr.CreateField(fieldDefn)
                # inlyr.DeleteField(17)
                feature=inlyr.GetNextFeature()
                while feature:
                    feature.SetField("filename", file_)
                    inlyr.SetFeature(feature)
                    feature=inlyr.GetNextFeature()

                # print("---Add column with name :", file_)

            if file_[-3:] == 'shp':
                shapefile_path = os.path.join(source, file_)
                shapefile_list.append(shapefile_path)
                infile = gdal.OpenEx(shapefile_path, gdal.GA_Update)
                fieldDefn = ogr.FieldDefn('dirname', ogr.OFTString)
                fieldDefn.SetWidth(254)
                inlyr = infile.GetLayer()
                # inlyr=inlyr.GetLayerDefn()
                inlyr.CreateField(fieldDefn)
                # inlyr.DeleteField(17)
                feature = inlyr.GetNextFeature()
                while feature:
                    feature.SetField("dirname", dirname)
                    inlyr.SetFeature(feature)
                    feature = inlyr.GetNextFeature()

                print ("---Add column with filename and dirname :", file_)
def AddSHPtoDATABASE():

    full_dir = os.walk(base_dir)
    shapefile_list = []
    for source, dirs, files in full_dir:
        for file_ in files:
            if file_[-3:] == 'shp':
                shapefile_path = os.path.join(source, file_)
                print(shapefile_path)
                shapefile_list.append(shapefile_path)
    print("---List of shapes witch would be added to data base :", shapefile_list)
    for shape_path in shapefile_list:
        cmds = 'shp2pgsql -a -g geom ' + shape_path + ' "new_shp_table_orto"  | psql '
        print("---Add this to database :", shape_path)
        subprocess.call(cmds, shell=True)

def create_buffer():
    cmds = 'psql -c "'"drop table footprint_polygon_test2_temp;create table footprint_polygon_test2_temp as select st_union(st_buffer(geom::geography,500)::geometry) as geom,field_2 as name,filename,dirname from new_shp_table where dirname="+"'"+dirname+"'"+" group by dirname,filename,field_2 order by dirname,filename,field_2; update footprint_polygon_test2_temp set name=REPLACE(name,'/','-');insert into footprint_polygon_test2 select * from footprint_polygon_test2_temp;"'"'
    subprocess.call(cmds, shell=True)
    print("URA!!")
#
# # ReplaceComasToDots()
# ConvertTXTtoCSV()
CreatingSHPfromCSV()
AddColunmsToSHP()
# AddSHPtoDATABASE()
#create_buffer()
