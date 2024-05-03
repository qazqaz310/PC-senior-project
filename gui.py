"""This is the main file for my project. It runs the GUI.
Run the file. This code is not for editing or maintenance"""

import PySimpleGUI as sg # Version 4.60.5 DO NOT UPDATE TO 5.0
from pathlib import Path
import os

# my imports!
from questionclasses import testQuestion, writeAnswerToFile, setupFile
from questionclasses import makeQuestionFromJSON, calculateScoreFromFile 

from makeatest import createQuestionGUI,writeToTest
from makeatest import defineLayoutNoInput, defineLayoutWithInput

# creating layouts and updating their visibility is the best/only way
# to create 'dynamic layouts' in PySimpleGUI. We make do with what we can.

#change the working directory.
script_location = Path(__file__).absolute().parent
os.chdir(script_location)

# this layout is shown when the program is ran.
def makeLayouts(questionData):
    layouts = []
    i = 0
    for q in questions:
        # if the question is multiple choice, use a dropdown box.
        if q.getMC() is True:
            layout = [
                [sg.Text(q.getQT())],
                [sg.Combo([f'{q}: {a}' for (q, a) in q.getPA().items()], 
                enable_events=True, key=f'--Q{i}--')]
            ]
        # otherwise, use a text input.
        elif q.getMC() is False:
            layout = [
                [sg.Text(q.getQT())],
                [sg.Input(enable_events=True,key=f'--Q{i}--')]
                ]
        # append the question to layouts and increment the counter
        layouts.append(layout)
        i += 1
    return layouts

opening_layout = [
    [sg.Text('welcome! Are you here to:')],
    [sg.Button('Take a test', key='--TAKER--'), 
     sg.Button('Create a test', key='--MAKER--')],
    [sg.Exit()]
]
# shown before taking a test.
layout_file_select = [
    [sg.Text("Browse for the test file:")],
    [sg.Input(size=(80, 1)), sg.FileBrowse(key='testPath')],
    [sg.Button('Submit'), sg.Button('back',key='--BACK1--')]
]

# larger layout contains other layouts as columns,
# allowing us to update their visibility on demand.
menu_layout = [
    [sg.Column(opening_layout, key='--COL1--',visible=True)],
    [sg.Column(layout_file_select, key='--COL2--',visible=False)]
]


# window1 is the first window people see.
window1 = sg.Window('App Home Screen', menu_layout, size=(640, 480))

# Routing tells us which screen we're on
routing = 'main'
# create an empty test path so we know if the user inputs one or not
testPath = ''
while True:
    event, values = window1.read()
    if event == sg.WIN_CLOSED or event == 'Exit':
        break
    # if they click take test, go to test browser layout
    if event == '--TAKER--':
        window1['--COL1--'].update(visible=False)
        window1['--COL2--'].update(visible=True)
    if event == '--MAKER--':
        routing = 'maker'
        break
    if event == '--BACK1--':
        window1['--COL1--'].update(visible=True)
        window1['--COL2--'].update(visible=False)

    if event == 'Submit':
        testPath = (values['testPath'])
        routing = 'TakeTest'
        if testPath == '':
            sg.popup('Please select file.')  
        else:
            break
window1.close()

if routing == 'TakeTest':
    questions = makeQuestionFromJSON(testPath)
    layouts = makeLayouts(questions)
    questions_layout = [
    [sg.Column(visible=True if i<1 else False, layout=q, key=f'--COL{i}--') 
     for (i,q) in enumerate(layouts)],
    [sg.Button('Next',key='--NEXT--'), sg.Button('Previous')]]
    # tracks the question we're looking at
    currentQ = 0
    window2 = sg.Window('test', questions_layout, size=(640, 480))
    # add a line to the output file for each question
    setupFile(len(layouts))
    while True:
        event, values = window2.read()
        if event == sg.WIN_CLOSED:
            break
        if event == '--NEXT--':
            # check if the next layout is invalid, then close the test.
            if currentQ >= (len(layouts) - 1):
                # calculate the score and show it in a popup.
                scores = calculateScoreFromFile()
                sg.popup(f'You scored {scores[0]} out of {scores[1]}.')
                break
            # if it will update to the last question, change 'next' to 'finish'.
            elif currentQ >= (len(layouts) - 2):
                window2['--NEXT--'].update('Finish')
            # then, update the visible window.
            window2[f'--COL{currentQ}--'].update(visible=False)
            currentQ += 1
            window2[f'--COL{currentQ}--'].update(visible=True)
        if event == 'Previous':
            # same thing backwards. If currently looking at the last question, 
            # change 'finish' back to 'next'.
            if currentQ >= (len(layouts) - 1):
                window2['--NEXT--'].update('Next')
            # then update the current window.
            window2[f'--COL{currentQ}--'].update(visible=False)
            currentQ -= 1
            window2[f'--COL{currentQ}--'].update(visible=True)

        # if there's an event in the dropdown box or the text input,
        if event == f'--Q{currentQ}--':
            # store it in currentQAnswer.
            currentQAnswer = (f'{values[f'--Q{currentQ}--']}').split(':')[0]
            # store the correct answer too.
            correctAnswer = questions[currentQ].getCA()
            # format the answer and correct answer together 
            # to write them to the file.
            # NOTE: writeAnswerToFile() looks at the characters 
            # BEFORE the colon.
            # to determine what question number we're looking at. 
            answer = f'{currentQ}: {currentQAnswer} {correctAnswer} {True if currentQAnswer == correctAnswer else False}'
            writeAnswerToFile(answer, currentQ)
    window2.close()

# if you're making a test, go here.
if routing == 'maker':
    # tracks whether we're making a new test or editing an old one.
    makerLayout = [
        [sg.Text('do you want to:')],
        [sg.Button('Make a new test',key='makeNew')],
        [sg.Text('OR')],
        [sg.Button('Edit a test',key='editOld')]
    ]
    # name input and folder browser.
    makeNewLayout = [
        [sg.Text('give your test a name and pick a place to put it!')],
        [sg.Text('Please no special characters (!@#$%^&* etc)')],
        [sg.Input(default_text='your name here',key='testName')],
        [sg.FolderBrowse(button_text='select a folder',key='folderBrowse')],
        [sg.Submit(key='makerSubmitNew')]
    ]
    # file select, only .json files
    editOldLayout = [
        [sg.Text('Pick a test to edit:')],
        [sg.FileBrowse(button_text='Select File',key='fileSelect'
                       ,file_types=(('json files', '*.json'),))],
        [sg.Submit(key='makerSubmitOld')]
    ]
    # create columns
    makerColumn = sg.Column(makerLayout,key='makerLayoutKey')
    makeNewLayoutColumn = sg.Column(makeNewLayout,key='makeNewLayoutKey',visible=False)
    editOldLayoutColumn = sg.Column(editOldLayout,key='editOldLayoutKey', visible=False)
    # create layout
    makerMasterLayout = [
        [makerColumn],
        [makeNewLayoutColumn],
        [editOldLayoutColumn]
    ]
    window3 = sg.Window('makerMasterLayout', makerMasterLayout)
    while True:
        ev3, val3 = window3.read()
        if ev3 == sg.WIN_CLOSED:
            break
        # if they click a button, update the visibility.
        if ev3 == 'makeNew':
            window3['makerLayoutKey'].update(visible=False)
            window3['makeNewLayoutKey'].update(visible=True)
        if ev3 == 'editOld':
            window3['makerLayoutKey'].update(visible=False)
            window3['editOldLayoutKey'].update(visible=True)
        # if they make a new one, give it the proper name, then open the maker.
        if ev3 == 'makerSubmitNew':
            folder = val3['folderBrowse']
            fileName = f'{val3['testName']}.json'
            filePath = os.path.join(folder,fileName)
            window3.close()
            qs = createQuestionGUI()
            writeToTest(qs, filePath)
            break
        # if they edit an old one, open it in the maker.
        if ev3 == 'makerSubmitOld':
            window3.close()
            filePath = val3['fileSelect']
            questions = makeQuestionFromJSON(filePath)
            qs = createQuestionGUI(questions=questions)
            writeToTest(qs, filePath)
            break