import PySimpleGUI as sg
# from questionclasses import testQuestion
import json
import os
from pathlib import Path
from questionclasses import testQuestion, makeQuestionFromJSON
# gets the main file location and change the working directory.
script_location = Path(__file__).absolute().parent
os.chdir(script_location)

def defineLayoutNoInput():
        """This function defiles a GUI layout without an input. Returns
        that layout."""
        # is the question multiple choice true or false question
        QMC = [
        [sg.Text('is the question multiple choice?'),
        sg.Radio('True','MultipleChoiceRadio',
            key='MultipleChoiceTrue',enable_events=True),
        sg.Radio('False','MultipleChoiceRadio',
            key='MultipleChoiceFalse',enable_events=True)]]
        # create a combo that determines the number of possible responses
        QCount = [[sg.Text('how many responses do you want?'),
                sg.Combo(['2','3','4','5'],enable_events=True,key='--COMBO--')]]
        # create an input for the question text
        QText = [[sg.Text('What is the Question?'),
                sg.Input(key='QuestionText',enable_events=True)]]
        QAnswer = [[sg.Text('What is the Answer?'),
                   sg.Input(enable_events=True,key='QuestionAnswer')]]
        # create layouts with a radio element, a label, and an input box.
        Q1PA = [
            [sg.Radio('','PossibleAnswersRadio',key='PossibleAnswersRadio1',
                enable_events=True),
            sg.Text('Answer 1:'),
            sg.Input(key='PossibleAnswersText1',enable_events=True)]]
        Q2PA = [
            [sg.Radio('','PossibleAnswersRadio',key='PossibleAnswersRadio2',
                enable_events=True),
            sg.Text('Answer 2:'),
            sg.Input(key='PossibleAnswersText2',enable_events=True)]]
        Q3PA = [
            [sg.Radio('','PossibleAnswersRadio',key='PossibleAnswersRadio3',
                enable_events=True),
            sg.Text('Answer 3:'),
            sg.Input(key='PossibleAnswersText3',enable_events=True)]]
        Q4PA = [
            [sg.Radio('','PossibleAnswersRadio',key='PossibleAnswersRadio4',
                enable_events=True),
            sg.Text('Answer 4:'),
            sg.Input(key='PossibleAnswersText4',enable_events=True)]]
        Q5PA = [
            [sg.Radio('','PossibleAnswersRadio',key='PossibleAnswersRadio5',
                enable_events=True),
            sg.Text('Answer 5:'),
            sg.Input(key='PossibleAnswersText5',enable_events=True)]]
        # turn each layout into a column.
        MCQ = sg.Column(QMC, key='MultipleChoiceTrueOrFalse')

        QT = sg.Column(QText, key='QuestionTextColumn')

        testMakerLayout = [
            # this layout defines the interactive elements between questions.
    [sg.Button('Next',key='--NEXT--'),sg.Button('Previous',key='--PREVIOUS--')],
    [sg.Button('Add',key='--ADDQ--'),sg.Button('Delete',key='--DELETEQ--'),
        sg.Button('Finish',key='--FIN--')]
            ]
        
        QCountColumn = sg.Column(QCount,key='QCountInput',visible=False)
        QAnswerCol = sg.Column(QAnswer, key='QAnswerColumn',visible=False)
        col1 = sg.Column(Q1PA, key='PossibleAnswerColumn1',visible=False)
        col2 = sg.Column(Q2PA, key='PossibleAnswerColumn2',visible=False)
        col3 = sg.Column(Q3PA, key='PossibleAnswerColumn3',visible=False)
        col4 = sg.Column(Q4PA, key='PossibleAnswerColumn4',visible=False)
        col5 = sg.Column(Q5PA, key='PossibleAnswerColumn5',visible=False)

        # define a layout with all the columns together
        layout = [
            [MCQ],
            [QT],
            [QCountColumn],
            [QAnswerCol],
            [col1],
            [col2],
            [col3],
            [col4],
            [col5],
            [testMakerLayout]
        ]
        return layout
    
def defineLayoutWithInput(testQuestion: testQuestion):
    """defines a layout given an already existing test question.
    returns that layout."""
    QMC = [
    # this time: select the appropriate value
    [sg.Text('is the question multiple choice?'),
     
    sg.Radio('True','MultipleChoiceRadio',key='MultipleChoiceTrue',
        enable_events=True,
        default=True if testQuestion.getMC() is True else False),

    sg.Radio('False','MultipleChoiceRadio',key='MultipleChoiceFalse', 
        enable_events=True,
        default=False if testQuestion.getMC() is True else True)]]
    
    # create a combo that determines the number of possible responses
    QCount = [
        [sg.Text('how many responses do you want?'),sg.Combo(['2','3','4','5'],
        enable_events=True,key='--COMBO--',
        default_value=len(testQuestion.getPA()))]
    ]
    # create an input for the question text
    QText = [[sg.Text('What is the Question?'),sg.Input(key='QuestionText',
            enable_events=True,default_text=testQuestion.getQT())]]
    QAnswer = [[sg.Text('What is the Answer?'),
                   sg.Input(enable_events=True,key='QuestionAnswer',
                    default_text=testQuestion.getCA())]]
    # create layouts with a radio element, a label, and an input box.
    # these are kind of gross because of the 80 char limit.
    Q1PA = [
        [sg.Radio('','PossibleAnswersRadio',key='PossibleAnswersRadio1',
        enable_events=True,default=True if testQuestion.getCA()=='a' else False)
        ,sg.Text('Answer 1:'),
        sg.Input(key='PossibleAnswersText1',
        enable_events=True,
        default_text = testQuestion.getPA()['a'] 
        if not testQuestion.getPA().get('a') == None else '')]]
    Q2PA = [
        [sg.Radio('','PossibleAnswersRadio',key='PossibleAnswersRadio2',
        enable_events=True,default=True if testQuestion.getCA()=='b' else False)
        ,sg.Text('Answer 2:'),sg.Input(key='PossibleAnswersText2',
        enable_events=True,default_text = testQuestion.getPA()['b']
        if not testQuestion.getPA().get('b') == None else '')]]
    Q3PA = [
        [sg.Radio('','PossibleAnswersRadio',key='PossibleAnswersRadio3',
        enable_events=True,default=True if testQuestion.getCA()=='c' else False)
        ,sg.Text('Answer 3:'),sg.Input(key='PossibleAnswersText3',
        enable_events=True,default_text = testQuestion.getPA()['c'] 
        if not testQuestion.getPA().get('c') == None else '')]]
    Q4PA = [
        [sg.Radio('','PossibleAnswersRadio',key='PossibleAnswersRadio4',
        enable_events=True,default=True if testQuestion.getCA()=='d' else False)
        ,sg.Text('Answer 4:'),sg.Input(key='PossibleAnswersText4',
        enable_events=True,default_text = testQuestion.getPA()['d'] 
        if not testQuestion.getPA().get('d') == None else '')]]
    Q5PA = [
        [sg.Radio('','PossibleAnswersRadio',key='PossibleAnswersRadio5',
        enable_events=True,default=True if testQuestion.getCA()=='e' else False)
        ,sg.Text('Answer 5:'),sg.Input(key='PossibleAnswersText5',
        enable_events=True,default_text = testQuestion.getPA()['e'] 
        if not testQuestion.getPA().get('e') == None else '')]]
    # turn each layout into a column.
    MCQ = sg.Column(QMC, key='MultipleChoiceTrueOrFalse')

    QT = sg.Column(QText, key='QuestionTextColumn')
    testMakerLayout = [
        # this layout defines the interactive elements between questions.
    [sg.Button('Next',key='--NEXT--'),sg.Button('Previous',key='--PREVIOUS--')],
    [sg.Button('Add',key='--ADDQ--'),sg.Button('Delete',key='--DELETEQ--'),
        sg.Button('Finish',key='--FIN--')]
            ]
    QCountColumn = sg.Column(QCount,key='QCountInput',
        visible=True if testQuestion.getMC() is True else False)
    QAnswerCol = sg.Column(QAnswer, key='QAnswerColumn',
        visible=False if testQuestion.getMC() is True else True)
    col1 = sg.Column(Q1PA, key='PossibleAnswerColumn1',
        visible=True if testQuestion.getMC() is True else False)
    col2 = sg.Column(Q2PA, key='PossibleAnswerColumn2',
        visible=True if testQuestion.getMC() is True else False)
    col3 = sg.Column(Q3PA, key='PossibleAnswerColumn3',
        visible=True if testQuestion.getMC() is True 
            and len(testQuestion.getPA()) >= 3 else False)
    col4 = sg.Column(Q4PA, key='PossibleAnswerColumn4',
        visible=True if testQuestion.getMC() is True 
            and len(testQuestion.getPA()) >= 4 else False)
    col5 = sg.Column(Q5PA, key='PossibleAnswerColumn5',
        visible=True if testQuestion.getMC() is True 
            and len(testQuestion.getPA()) == 5 else False)

    # define a layout with all the columns together
    layout = [
        [MCQ],
        [QT],
        [QCountColumn],
        [QAnswerCol],
        [col1],
        [col2],
        [col3],
        [col4],
        [col5],
        [testMakerLayout]
    ]
    return layout

def writeToTest(args,filePath):
    """writes a list of test questions to an output file."""
    testList = [q.to_json() for q in args]
    tempDict = {
        'Title': 'test',
        'author': 'Otis',
        'questions': testList
    }
    json_object = json.dumps(tempDict, indent=4)
    with open(filePath, 'w') as outfile:
        outfile.write(json_object)
    return None

def createQuestionGUI(index=None, arg = None,questions=None,recursive=False):
    # this gets used to convert numbers to letters for tracking questions
    translator = {1: 'a', 2: 'b', 3:'c', 4:'d', 5: 'e'}
    if index is None:
        index = 0
    if questions is None:
        questions = []
    if len(questions) != 0 and recursive is False:
        arg = questions[index]
    def answersSetVisibility(new: int, previous: int, multipleChoice: bool):
        """takes two values, the new quantity of responses and the previous.
        changes the number of visible inputs to the new one."""
        # if the new is higher than the old,
        if new > previous:
            # just make the new ones visible and update the possibleanswers dict
            i = previous
            while i <= new:
                window[f'PossibleAnswerColumn{i}'].update(visible=True)
                possibleAnswers.update({translator[i]: ''})
                i += 1
        # if the old is higher than the new,
        elif previous > new:
            # unclick the boxes if they're there, 
            # empty the text boxes, and make them invisible.
            i = previous
            while i > new:
                window[f'PossibleAnswerColumn{i}'].update(visible=False)
                window[f'PossibleAnswersRadio{i}'].update(value=False)
                window[f'PossibleAnswersText{i}'].update(value='')
                # update the possibleanswers dictionary.
                if multipleChoice is True:
                    del possibleAnswers[translator[i]] 
                i -= 1
    
    # if we are editing a question,
    if type(arg) == testQuestion:
        # change all the default values and make set the init value
        MultipleChoice = arg.getMC()
        questionText = arg.getQT()
        selectedAnswer = arg.getCA()
        possibleAnswers = (arg.getPA().copy())
        layout = defineLayoutWithInput(arg)
        init = True
    else:
        # otherwise set everything up the easy way
        layout = defineLayoutNoInput()
        questionText = ''
        selectedAnswer = ''
        possibleAnswers = {}
        MultipleChoice = None
        init = False
    
    window = sg.Window('Test Maker', layout)
    
    # track all the possible answers
    QCountInput = 1
    while True:
        ev1, val1 = window.read()
        if ev1 == sg.WIN_CLOSED:
            break
        if init is True:
            QCountTemp = QCountInput
            QCountInput = int(val1['--COMBO--'])
            answersSetVisibility(int(QCountInput), int(QCountTemp),arg.getMC())
            for _ in range(QCountInput):
                possibleAnswers.update({translator.get(_+1): 
                                        val1[f'PossibleAnswersText{_+1}']})
            init = False

        
        if ev1 == 'MultipleChoiceTrue':
            MultipleChoice = True
            window['QCountInput'].update(visible=True)
            window['QAnswerColumn'].update(visible=False)
            selectedAnswer = ''
            
        if ev1 == 'MultipleChoiceFalse':
            MultipleChoice = False
            window['QAnswerColumn'].update(visible=True)
            window['QCountInput'].update(visible=False)
            window['PossibleAnswerColumn1'].update(visible=False)
            window['PossibleAnswerColumn2'].update(visible=False)
            window['PossibleAnswerColumn3'].update(visible=False)
            window['PossibleAnswerColumn4'].update(visible=False)
            window['PossibleAnswerColumn5'].update(visible=False)
            possibleAnswers = {}
            selectedAnswer = ''

        if ev1 == 'QuestionAnswer':
            selectedAnswer = val1['QuestionAnswer']

        if ev1 == '--COMBO--':
            # store the previous value
            QCountTemp = QCountInput
            QCountInput = int(val1['--COMBO--'])
            answersSetVisibility(int(QCountInput), int(QCountTemp),MultipleChoice)
        
        for _ in range(QCountInput):
            if ev1 == f'PossibleAnswersRadio{_+1}':
                selectedAnswer = translator.get(_+1)
        
        for _ in range(QCountInput):
            if ev1 == f'PossibleAnswersText{_+1}':
                possibleAnswers.update({translator.get(_+1): 
                                        val1[f'PossibleAnswersText{_+1}']})
        
        if ev1 == 'QuestionText':
            questionText = val1['QuestionText']

        if ev1 == '--NEXT--':
            window.close()
            if questions[index]:
                questions[index] = testQuestion(questionText, MultipleChoice, 
                                str(selectedAnswer), possibleAnswers)
            else:
                questions.append(testQuestion(questionText, MultipleChoice, 
                                str(selectedAnswer), possibleAnswers))
            index += 1
            createQuestionGUI(index, questions=questions, arg=questions[index],recursive=True)
        if ev1 == '--PREVIOUS--':
            window.close()
            try:
                questions[index] = testQuestion(questionText, MultipleChoice, 
                                str(selectedAnswer), possibleAnswers)
            except IndexError:
                questions.append(testQuestion(questionText, MultipleChoice, 
                                str(selectedAnswer), possibleAnswers))   
            index -= 1
            createQuestionGUI(index,questions=questions,arg=questions[index],recursive=True)
        if ev1 == '--ADDQ--':
            window.close()
            try:
                questions[index]
            except IndexError:
                questions.append(testQuestion(questionText, MultipleChoice, 
                                str(selectedAnswer), possibleAnswers))
            else:
                questions[index] = testQuestion(questionText, MultipleChoice, 
                                str(selectedAnswer), possibleAnswers)
            index += 1
            questions.insert(index, None)
            createQuestionGUI(index,questions=questions,recursive=True)
        if ev1 == '--DELETEQ--':
            window.close()
            questions.pop(index)
            if not index == 0:
                index -= 1
            createQuestionGUI(index,questions=questions,
                            arg=questions[index],recursive=True)
                
        if ev1 == '--FIN--':
            window.close()
            try:
                questions[index]
            except IndexError:
                questions.append(testQuestion(questionText, MultipleChoice, 
                                str(selectedAnswer), possibleAnswers))
            else:
                questions[index] = testQuestion(questionText, MultipleChoice, 
                                str(selectedAnswer), possibleAnswers)
            break
    return questions

if __name__ == '__main__':
    questions = makeQuestionFromJSON('./testsAndResults/space quiz.json')
    questions = createQuestionGUI(questions=questions)
    writeToTest(questions, './testsAndResults/space quiz.json')
