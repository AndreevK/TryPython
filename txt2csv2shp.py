import os
import csv

root_path = os.path
for dir in os.walk(root_path):
     for txt_file in dir[2]:
         if txt_file[-3:]=='txt':
            csv_file = os.path.join(os.path.dirname(txt_file),os.path.basename(txt_file)[:-3]+'csv')
            os.chdir(dir[0])
            in_txt = csv.reader(open(txt_file,"rb"), delimiter = '\t')
            out_csv = csv.writer(open(csv_file, 'wb'))
            out_csv.writerows(in_txt)

root_path1 = os.path
for dir in os.walk(root_path1):
     for file_name in dir[2]:
         if file_name[-3:]=='csv':
             os.chdir(dir[0])
             fname=file_name[0:-4]
             fvrt = open(fname+'.vrt', 'wt')
             fvrt.write('<OGRVRTDataSource>\n'
                        '<OGRVRTLayer name="'+fname+'">\n'
                        '<SrcDataSource>'+fname+'.csv</SrcDataSource>\n'
                        '<GeometryType>wkbPoint</GeometryType>\n'
                        '<LayerSRS>WGS84</LayerSRS>\n'
                        '<GeometryField encoding="PointFromColumns" x="field_12" y="field_13"/>\n'
                        '</OGRVRTLayer>\n'
                        '</OGRVRTDataSource>\n')
             fvrt.close()
             os.system('ogr2ogr '+fname+'.shp '+fname+'.vrt')
             os.system('del '+fname+'.vrt') 


     

    


         



