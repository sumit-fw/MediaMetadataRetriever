'''
Created on Jan 8, 2019

@author: sumit
''' 
import glob, os, shutil
from builtins import str
from Lib import Report




def MoveFiles(source,destination,filetype):
    '''
    Move files from source folder to destination folder.
    :param source
    :param destination
    :param filetype
    '''
    files = glob.iglob(os.path.join(source, '*'+filetype))
    for file in files:
        if os.path.isfile(file):
            shutil.move(src=file, dst=destination)




def JsonValue(json_data,key, result={}):
    for k in json_data:
        if k==key:
            if not result=={}:
                result
            else:
                result=json_data[k]
            return result
        elif isinstance(json_data[k], dict):
            result=JsonValue(json_data[k], key, result)
        elif isinstance(json_data[k], list):
            for i in json_data[k]:
                result=JsonValue(i, key, result)
        elif isinstance(json_data[k], str):
            pass
        else:
            continue
    return(result)


def expectedjson(actual, expected):
    temp=JsonValue(expected, str(actual["height"]))
    fps=actual["avg_frame_rate"]
    temp1=CustomReturn('avg_frame_rate', fps)
    str_fps=round(int(temp1),0)
    match=JsonValue(temp, str(str_fps))
    return match
    
    
def CustomReturn(key, value):
    if key == "avg_frame_rate":
        
        #ret=int(int(value[:5])/1000)
        ret=value.split('/')
        value=int(ret[0])/int(ret[1])        
        return round(value,0)
    elif key == "bit_rate":
        ret=int(value)/1002001
        return int(ret)
    else:
        return value


def CustomValidate(key, actual, expected):
    if key == "width":
        return True if actual == expected else False
    elif key == "height":
        return True if actual == expected else False
    elif key == "avg_frame_rate":
        return True if CustomReturn(key, actual) == expected else False
    elif key == "bit_rate":
        return True if CustomReturn(key, actual) == expected else False
    else:
        if actual == expected:            
            return True
        else:
            return False



def custom_split(string,key):
    string = string.strip(' ,[,]')    
    return string.split(key)
    

def gps_dump(gps_json, file, reportfolder, json_object):
    header=[]
    workbook=Report.initExcel(reportfolder,file)
    for key in gps_json:
        if type(gps_json[key])==str:
            header.append(gps_json[key])
        if type(gps_json[key])==dict:
            if not workbook.get_worksheet_by_name(key):
                worksheet = workbook.add_worksheet(key)
            else:
                worksheet = workbook.get_worksheet_by_name(key)
            gps_map(worksheet=worksheet, header=header, title=gps_json[key],  json_object=json_object,key =key)    
    Report.deinitExcel(workbook)


def gps_map(worksheet, header, title, json_object,key):
    col= 0
    
    for i in range(len(json_object[key])):
        row=0
        for temp in header:
            worksheet.write(row,col,temp)
            worksheet.write(row,col+1,json_object[temp][i])
            row+=1
        cell=col
        for ti in title:
            worksheet.write(row,cell,title[ti])
            cell+=1
        row+=1
        num=0
        cell=col+num
        for value in custom_split(string=json_object[key][i], key=","):
            if cell>=col+len(title)-1: 
                worksheet.write(row,cell,int(value))
                cell=col
                row+=1
            else:
                worksheet.write(row,cell,int(value))
                cell+=1
                
        col=col+len(title)+2
           
if __name__ == '__main__':
    pass