'''
Created on Jan 6, 2019

@author: Sumit
'''

import os
from Lib import LibUtils
from Lib import Report

#from Lib import Ui
#from test import worksheet

def VideoCheckIntegrity(workbook, reportfolder, files, mediafiles):
    '''
    Check integrity of MP4 files.
    :param workbook
    :param reportfolder
    :param files
    '''
    if not workbook.get_worksheet_by_name("Integrity"):
        worksheet = workbook.add_worksheet("Integrity")
    else:
        worksheet=workbook.get_worksheet_by_name("Integrity")
    # Add a bold format to use to highlight cells.
    bold = workbook.add_format({'bold': 1, 'bg_color':'#75A5D0','border':1})
    
    # Write some data headers.
    worksheet.write('A1', 'File Name', bold)
    worksheet.write('B1', 'Result', bold)
    
    
    desfolder=Report.CreateFolder(folder=reportfolder, foldername='integrity_check')
    row, col = 1, 0
    for file in files:
        ffprobe_command = '.\\Tools\\ffmpeg.exe'+ ' ''-v error -i '+'"' +mediafiles[file] +'"'+' '+ '-map 0:1 -f null - 2> '+'"'+desfolder+'\\'+'integrity_check_'+file+'.log'+'"'
        output = os.system(ffprobe_command)
        if output == 0:
            worksheet.write(row, col,file)
            worksheet.write(row, col+1,"PASS")
            row+=1
        else:
            worksheet.write(row, col,file)
            worksheet.write(row, col+1,"FAIL")
            row+=1
    #Ui.Msg("Done")

def VideoGeneralProperties(workbook, reportfolder, files, mediafiles): 
    '''
    Check General Properties of MP4 files.
    :param workbook
    :param reportfolder
    :param files
    '''
    checkmetadata=Report.Loadjson(file=".\\config\\general_properties.json")
    desfolder=Report.CreateFolder(folder=reportfolder, foldername='general_properties')
    
    
    if not workbook.get_worksheet_by_name("GeneralProperties"):
        worksheet = workbook.add_worksheet("GeneralProperties")
    else:
        worksheet=workbook.get_worksheet_by_name("GeneralProperties")
        
    # Add a bold format to use to highlight cells.
    heading = workbook.add_format({'bold': 1, 'bg_color':'#75A5D0','border':1})
    red = workbook.add_format({'bg_color':'red','border':1})
    green = workbook.add_format({'bg_color':'green','border':1})
    yellow = workbook.add_format({'bg_color':'yellow','border':1})
    row, col = 0, 1
    
    # Write some data headers.
    worksheet.write(0,0,"FileName", heading)
    for i in checkmetadata["Check"]:
        worksheet.write(row,col,checkmetadata["Check"][i], heading)
        col+=1
    row+=1
    for file in files:
        general_file=desfolder+'\\'+'general_properties_'+file+'.log'
        #audio_file=desfolder+'\\'+'audio_properties_'+file+'.log'+'"'
        ffprobe_command = '.\\Tools\\ffprobe.exe'+ ' ''-hide_banner -loglevel fatal -show_error -show_format -show_streams -show_programs -show_chapters -show_private_data -print_format json ' +'"'+mediafiles[file]+'"'+'>'+'"'+general_file
        #ffmpeg_command = '.\\Tools\\ffmpeg.exe'+ ' ''-i ' +'"'+files[file]+'"'+ ' ''-filter:a volumedetect -f null - 2>'+'"'+audio_file
        os.system(ffprobe_command)
        #os.system(ffmpeg_command)
        
        actualmeta=Report.GeneralReport(filename=file, logfile=Report.Loadjson(general_file), checkmetadata=checkmetadata["Check"])
        match=LibUtils.expectedjson(actual=actualmeta, expected=checkmetadata)
        col=0
        for key in actualmeta:
            if LibUtils.JsonValue(match, key)=={}:
                worksheet.write(row, col, LibUtils.CustomReturn(key, actualmeta[key]),yellow)
            elif LibUtils.CustomValidate(key, actual=LibUtils.JsonValue(actualmeta, key), expected=LibUtils.JsonValue(match, key)):
                worksheet.write(row, col, LibUtils.CustomReturn(key, actualmeta[key]),green)
            elif LibUtils.JsonValue(actualmeta, key)!=LibUtils.JsonValue(match, key):
                worksheet.write(row, col, LibUtils.CustomReturn(key, actualmeta[key]),red)
            else:
                worksheet.write(row, col, LibUtils.CustomReturn(key, actualmeta[key]))
            col+=1
        row+=1
    #Ui.Msg("Done")

def VideoCustom(workbook, reportfolder, folder, files, mediafiles, customsetup):
    '''
    Generate Generate Report with all input files.
    :param reportfolder
    :param folder
    :param files
    '''
    if not workbook.get_worksheet_by_name("Custom"):
        worksheet = workbook.add_worksheet("Custom")
    else:
        worksheet = workbook.get_worksheet_by_name("Custom")
    # Add a bold format to use to highlight cells.
    bold = workbook.add_format({'bold': 1, 'bg_color':'#75A5D0','border':1})
    obrder=workbook.add_format({'bg_color':'yellow','border':1})
    # Write some data headers.
    

    
    FILES = [f for f in files if f.endswith('.MP4') or f.endswith('.LRV') or f.endswith('.mp4') or f.endswith('.360')]
    desfolder=Report.CreateFolder(folder=reportfolder, foldername='Custom')
    for file in FILES:
        command = customsetup+ ' ' +'"'+folder+'\\'+ file+'"'
        _=os.system(command)

    LibUtils.MoveFiles(folder, desfolder, "json")
    row = 0
    
    checkmetadata=Report.Loadjson(file="D:\\config.json")    
    try:
        #pass
        print('temp')
        #gpsdata=Report.Loadjson(file="D:\\gps.json")
    except:
        #gpsdata={}
        print("gps config file not found")    
    worksheet.write('A1', 'File Name', bold)
    col=1
    for key in checkmetadata:
        #print(checkmetadata[key])
        worksheet.write(row, col, str(checkmetadata[key]),bold)
        col=col+1
    for file in FILES:
        row+=1
        col=1
        worksheet.write(row, 0, str(file),bold)
        logfile=desfolder+'\\'+file+'.json'
        json_object=Report.Loadjson(logfile, status='N')
        
        for key in checkmetadata:
            try:
                ret=json_object[key]
                worksheet.write(row, col, str(ret))
            except:
                ret='Tag not available'
                worksheet.write(row, col, str(ret),obrder)
            col+=1
        
        #if gpsdata != {}:
        #    LibUtils.gps_dump(gps_json=gpsdata, file=file, reportfolder=reportfolder, json_object=json_object)
        #else:
        #    print("GPS config not found")
        
        
        
    #Ui.Msg("Done")



def PhotoGeneralProperties(workbook, reportfolder, files, mediafiles):
    '''
    Check General Properties of MP4 files.
    :param workbook
    :param reportfolder
    :param files
    '''
    checkmetadata=Report.Loadjson(file=".\\config\\photo_general_properties.json")
    desfolder=Report.CreateFolder(folder=reportfolder, foldername='photo_general_properties')
    
    
    if not workbook.get_worksheet_by_name("PhotoGeneralProperties"):
        worksheet = workbook.add_worksheet("PhotoGeneralProperties")
    else:
        worksheet=workbook.get_worksheet_by_name("PhotoGeneralProperties")
        
    # Add a bold format to use to highlight cells.
    heading = workbook.add_format({'bold': 1, 'bg_color':'#75A5D0','border':1})
    red = workbook.add_format({'bg_color':'red','border':1})
    green = workbook.add_format({'bg_color':'green','border':1})
    yellow = workbook.add_format({'bg_color':'yellow','border':1})
    row, col = 0, 0
    
    # Write some data headers.
    #worksheet.write(0,0,"FileName", heading)
    for i in checkmetadata["Check"]:
        worksheet.write(row,col,checkmetadata["Check"][i], heading)
        col+=1
    row+=1
    
    for file in files:
        json_file=desfolder+'\\'+'photo_general_properties_'+file+'.log'
        ffprobe_command = '.\\Tools\\exiftool.exe -json -U'+ ' "'+mediafiles[file]+'" > "'+json_file+'"'
        os.system(ffprobe_command)

        logfile=Report.Loadjson(json_file)
        dump=checkmetadata["Check"]
        col=0
        #print(logfile[0])
        for key in dump:
            data=LibUtils.JsonValue(json_data=logfile[0], key=key)
                        
            match=LibUtils.JsonValue(checkmetadata['Validation'], key)
            
            if match=={}:
                worksheet.write(row, col, str(data),yellow)
            elif data == match:
                worksheet.write(row, col, str(data),green)
            elif data != match:
                worksheet.write(row, col, str(data),red)
            else:
                worksheet.write(row, col, str(data))
                
            
            #worksheet.write(row, col, str(data),yellow)
            col+=1
        row+=1
        

def PhotoCustom(workbook, reportfolder, folder, files, mediafiles, customsetup):
    '''
    Generate Generate Report with all input files.
    :param reportfolder
    :param folder
    :param files
    '''
    if not workbook.get_worksheet_by_name("PhotoCustom"):
        worksheet = workbook.add_worksheet("PhotoCustom")
    else:
        worksheet = workbook.get_worksheet_by_name("PhotoCustom")
    # Add a bold format to use to highlight cells.
    bold = workbook.add_format({'bold': 1, 'bg_color':'#75A5D0','border':1})
    obrder=workbook.add_format({'bg_color':'yellow','border':1})
    # Write some data headers.
    checkmetadata=Report.Loadjson(file="D:\\Photo_config.json")

    FILES = [f for f in files if f.endswith('.JPG') or f.endswith('.jpg')  or f.endswith('.Jpg')]
    desfolder=Report.CreateFolder(folder=reportfolder, foldername='PhotoCustom')
    for file in FILES:
        command = customsetup+ ' ' +'"'+folder+'\\'+ file+'"'
        _=os.system(command)

    LibUtils.MoveFiles(folder, desfolder, "json")
    row = 0
    
    worksheet.write('A1', 'File Name', bold)
    col=1
    for key in checkmetadata:
        worksheet.write(row, col, str(checkmetadata[key]),bold)
        col=col+1
    for file in FILES:
        row+=1
        col=1
        worksheet.write(row, 0, str(file),bold)
        #print(file)
        logfile=desfolder+'\\'+file+'.json'
        json_object=Report.Loadjson(logfile, status='N')
        print(json_object)
        for key in checkmetadata:
            try:
                ret=json_object[key]
                #ret=LibUtils.JsonValue(json_object,key)
                worksheet.write(row, col, str(ret))
            except:
                ret='Tag not available'
                worksheet.write(row, col, str(ret),obrder)
            col+=1
        
     
if __name__ == '__main__':
    pass
