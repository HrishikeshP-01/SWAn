import PySimpleGUI as sg
import os.path

import Selector

beingConverted = False
url = ''

# First the window layout
url_list_column = [
    [
        sg.Text("Enter URL:"),
        sg.In(size=(70,1),enable_events=True,key="-URL-"),
        sg.Button("Go"),
        ],
    [
        sg.Text("Select Scanner:"),
        sg.Combo(
            ["Web Crawler",
             "XSS Vulnerability Scanner",
             "SQL Injection Vulnerability Scanner"],
            enable_events = True, size=(30,1),key="-SCAN TYPE-")
        ],
    [
        sg.Listbox(
            values=[], enable_events=True, size=(150,30), key="-RET LIST-"),
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
        combo = values["-SCAN TYPE-"]
        url = values["-URL-"]
        ret_list = Selector.perform_analysis(combo,url)
        window["-RET LIST-"].update(ret_list)

window.close()
