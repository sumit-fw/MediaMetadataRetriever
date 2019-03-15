'''
Created on Jan 4, 2019

@author: sumit
'''
import PySimpleGUI.PySimpleGUI as sg
import os

# ----====----====----==== Constants the user CAN safely change ====----====----====----#
DEFAULT_WINDOW_TITLE = 'Media Metadata Retriever'



def Msg(args):
    sg.Popup(args)
    


def GetFolder(msg, title=DEFAULT_WINDOW_TITLE):
    '''
    UI application return Directory and list of files.
    :param msg
    :param title
    '''
    return sg.PopupGetFolder(msg,title)
    

def ShowFiles(reportfolder, file):
    '''
    UI application return filepath and list of files.
    '''
    layout=[
        [sg.Text('Reports:'),sg.Text(reportfolder)],
        [sg.Button('Video', size=(10,1)),sg.Button('Photo', size=(10,1))],
        [sg.Listbox(values=file, key='_FILE_', size=(35,10), select_mode = sg.LISTBOX_SELECT_MODE_MULTIPLE)],
        [sg.Button('Check Integrity', size=(35,1))],
        [sg.Button('General Properties', size=(35,1))],
        [sg.Button('Custom', size=(35,1))],
        [sg.Exit('Exit', size=(35,1))]
    ]
    
    return layout


if __name__ == '__main__':
    pass