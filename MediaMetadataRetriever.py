'''
Created on Dec 26, 2018

@author: Sumit
'''
from Lib import Ui
from Lib import Report
from Lib import Lib

SELECT_FOLDER="Please Select Directory that contain MP4 files"



#work
def main():
    folder=Ui.GetFolder(SELECT_FOLDER)
    if Report.DirCheck(folder):
        mediafiles=Report.GetFiles(folder)
        reportfolder=Report.CreateFolder(folder)
        workbook= Report.initExcel(reportfolder)
        
        files=Report.GetMp4Files(folder)
        window=Ui.ShowFiles(reportfolder,file=files)
        while True:      
            event, values = window.Read()
            if event is None or event == 'Exit':      
                break
            elif event == 'Check Integrity':
                Lib.CheckIntegrity(workbook, reportfolder,values['_FILE_'],mediafiles=mediafiles)
            elif event == 'General Properties':
                Lib.GeneralProperties(workbook, reportfolder,values['_FILE_'],mediafiles=mediafiles)
            elif event == 'Custom':
                Lib.Custom(workbook, reportfolder,folder,files=values['_FILE_'],mediafiles=mediafiles,customsetup='D:\\a.exe')
            else:
                pass 
        window.Close()
        Report.deinitExcel(workbook)
    else:
        print("Folder not found")

if __name__ == '__main__':
    main()
    