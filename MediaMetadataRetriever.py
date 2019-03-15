'''
Created on Dec 26, 2018

@author: Sumit
'''
from Lib import Ui
from Lib import Report
from Lib import Lib
import PySimpleGUI.PySimpleGUI as sg

SELECT_FOLDER="Please Select Directory that contain MP4 files"
DEFAULT_WINDOW_TITLE = 'Media Metadata Retriever'


#work
def main():
    folder=Ui.GetFolder(SELECT_FOLDER)
    if Report.DirCheck(folder):
        
        # Getting Media files
        mediafiles=Report.GetFiles(folder)
        Video_files=Report.GetMp4Files(folder)
        photo_files=Report.GetJPGFiles(folder)

        # Creating Report folder and workbook
        reportfolder=Report.CreateFolder(folder)
        workbook= Report.initExcel(reportfolder)
        
        # Creating layout for showing media files
        layout=Ui.ShowFiles(reportfolder,file=Video_files)
        window = sg.Window(DEFAULT_WINDOW_TITLE, default_element_size=(40, 1), grab_anywhere=False).Layout(layout)

        filetype='Video'        
        while True:      
            event, values = window.Read()
            if event is None or event == 'Exit':      
                break
            elif event == 'Photo':
                filetype='Photo'
                window.FindElement('_FILE_').Update(photo_files)
            elif event == 'Video':
                filetype='Video'
                window.FindElement('_FILE_').Update(Video_files)
            elif event == 'Check Integrity' and filetype =='Video':
                print(filetype)
                Lib.VideoCheckIntegrity(workbook, reportfolder,values['_FILE_'],mediafiles=mediafiles)
            elif event == 'General Properties' and filetype =='Video':
                Lib.VideoGeneralProperties(workbook, reportfolder,values['_FILE_'],mediafiles=mediafiles)
            elif event == 'Custom' and filetype =='Video':
                Lib.VideoCustom(workbook, reportfolder,folder,files=values['_FILE_'],mediafiles=mediafiles,customsetup='D:\\a.exe')
            elif event == 'General Properties' and filetype =='Photo':
                Lib.PhotoGeneralProperties(workbook, reportfolder,values['_FILE_'],mediafiles=mediafiles)
            else:
                pass 
            
        window.Close()
        Report.deinitExcel(workbook)
    else:
        print("Folder not found")

if __name__ == '__main__':
    main()
    