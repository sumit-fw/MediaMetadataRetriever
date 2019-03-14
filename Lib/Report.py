'''
Created on Jan 4, 2019

@author: sumit
'''
import os
import xlsxwriter
import json

try:
    from Lib import LibUtils
except:
    pass
    #import LibUtils

def DirCheck(folder):
    '''
    Return True if Directory Exist else False.
    :param Directory
    '''    
    return True if folder and os.path.isdir(folder) else False
    
    
def GetFiles(folder=""):
    '''
    Return List of files(MP4 LRV JPG).
    :param folder
    '''    
    FilesDic={}
    files = [f for f in os.listdir(folder) if f.endswith('.MP4') or f.endswith('.mp4')]
    for count in range(len(files)):
        FilesDic[str(files[count])]=os.path.join(folder,str(files[count]))
    return FilesDic

def GetMp4Files(folder=""):
    '''
    Return List of files(MP4).
    :param folder
    '''  
    FILES = [f for f in os.listdir(folder) if f.endswith('.MP4') or f.endswith('.mp4')]
    return(FILES)

def GetLRVFiles(folder=""):
    '''
    Return List of files(LRV).
    :param folder
    '''  
    FILES = [f for f in os.listdir(folder) if f.endswith('.LRV')]
    return(FILES)

def GetJPGFiles(folder=""):
    '''
    Return List of files(JPG).
    :param folder
    '''  
    FILES = [f for f in os.listdir(folder) if f.endswith('.JPG')]
    return(FILES)


def CreateFolder(folder="", foldercount=1, foldername='Report'):
    '''
    Create folder with name Report_x(x will be integer value)
    :param folder
    :param foldername
    :param foldercount
    '''
    reportfolder=os.path.join(folder,foldername+'_'+str(foldercount))
    try:
        if not DirCheck(reportfolder):
            os.makedirs(reportfolder)
            return reportfolder
        else:
            return reportfolder if [f for f in os.listdir(reportfolder) if not f.startswith('.')] == [] else CreateFolder(folder ,foldercount=int(foldercount)+1)
    except OSError:
        print ('Error: Creating directory. ' +  foldercount)
    
    
def initExcel(reportfolder, file='Report'):
    '''
    Create Excel with name Report_x(x will be integer value)
    :param reportfolder
    '''
    # Create an new Excel file and add a worksheet.
    workbook = xlsxwriter.Workbook(reportfolder+'\\'+file+'.xlsx')
    return workbook
    
    

def GeneralReport(filename, logfile, checkmetadata):
    result={}
    json_data=logfile
    result['name']=filename
    for key in checkmetadata:
        temp=LibUtils.JsonValue(json_data, key)
        if temp=={}:
            result[key]="Data Not Found in json"
        else:
            result[key]=LibUtils.JsonValue(json_data, key)
    return result

def deinitExcel(workbook):
    workbook.close()
    
def Loadjson(file):    
    with open(file) as f:
        try:
            json_data=json.load(f)
        except:
            json_data={}
            f.seek(0)
            for line in f:
                if ':' in line:
                    min_vol = line.split(':')
                    min_vol[0] = min_vol[0].strip(' ,\n,\"')
                    min_vol[1] = min_vol[1].strip('\,,\n, ,\"')
                    
                    key=str(min_vol[0])
                    value=str(min_vol[1])
                    
                    if key in json_data:
                        json_data[str(key)].append(str(value))
                    else:
                        json_data[str(key)]=[]
                        json_data[str(key)].append(str(value))
    return json_data

if __name__ == '__main__':
    pass