import PySimpleGUI as sg
import os.path

beingConverted = False
url = ''

# First the window layout
url_list_column = [
    [
        sg.Text("Enter URL:"),
        sg.In(size=(25,1),enable_events=True,key="-FOLDER-"),
        sg.Button("Go"),
        ],
    [
        sg.Combo(
            ["Web Crawler",
             "XSS Scanner",
             "SQL Injection Scanner"],
            enable_events = True, size=(50,1),key="-SCAN TYPE-")
        ],
    [
        sg.Listbox(
            values=[], enable_events=True, size=(40,20), key="-FILE LIST-"),
        ],
    ]

# Full layout
layout = [
    [
    sg.Column(url_list_column),
    ]
    ]
window = sg.Window("SWAn",layout)

# Run the Event Loop
while True:
    event, values = window.read()
    if event == "Exit" or event == sg.WIN_CLOSED:
        break
    # URL was filled in, perform analysis
    if event == "Go":
        beingConverted = True
        print("Done")

window.close()
