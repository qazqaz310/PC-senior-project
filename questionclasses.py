import json
import PySimpleGUI as sg
import os
from pathlib import Path

# gets the main file location and change the working directory.
script_location = Path(__file__).absolute().parent
os.chdir(script_location)

class testQuestion:
    '''
    this class is a container for data on a single test question.
    takes attributes:
        str questionText: the question's text
        bool multipleChoice: whether the question is multiple choice
        (true) or false
        str correctAnswer: the correct answer
        (expressed as a/b/c/d for multiple choice questions)
        list possibleAnswers: key pairs of possible answers (keys being a/b/c/d) 
        or None if the question isn't multiple choice)

    methods:
    def getMC():
        returns bool whether or not the question is multiple choice
    def getQT():
        returns string questionText
    def getCA():
        returns string correctAnswer
    def getPA():
        returns dict of possible answers and their keys, 
        or empty list of the question isn't multiple choice
        
    '''
    def __init__(self, questionText, multipleChoice, 
                 correctAnswer,possibleAnswers=None):
        self.multipleChoice = multipleChoice
        self.questionText = questionText
        self.correctAnswer = correctAnswer
        if possibleAnswers is None:
            possibleAnswers = {}
        self.possibleAnswers = possibleAnswers
    def getMC(self):
        return self.multipleChoice
    def getQT(self):
        return self.questionText
    def getCA(self):
        return self.correctAnswer
    def getPA(self):
        return self.possibleAnswers
    def __str__(self):
        return f'{self.multipleChoice}, {self.questionText}, {self.correctAnswer}, {self.possibleAnswers}'
    def __repr__(self):
        return f'({self.multipleChoice}, {self.questionText}, {self.correctAnswer}, {self.possibleAnswers})'
    def to_json(self):
        return {
            'multipleChoice': self.multipleChoice,
            'question': self.questionText,
            'possibleAnswers': self.possibleAnswers,
            'correctAnswer': self.correctAnswer
        }


def makeQuestionFromJSON(filePath):
    '''
    takes a filepath for a test (JSON file), 
    and returns question objects for each question in the test.
    returns a list of testQuestion objects.
    '''
    with open(filePath, 'r') as file:
        data = json.load(file)
    questions = []
    # look for the list called questions,
    # each question in it should be its own dictionary.
    for q in data['questions']:
        # not sure why this works. it does though, not messing with it anymore.
        if q['multipleChoice'] == True:
            questions.append(testQuestion(q['question'], q['multipleChoice'], 
                                    q['correctAnswer'],q['possibleAnswers']))
        elif q['multipleChoice'] == False:
            questions.append(testQuestion(q['question'], 
                        q['multipleChoice'], q['correctAnswer']))
    print(questions)
    return questions



def writeAnswerToFile(answer,qNumber):
    """Writes to a file, each line getting a separate question.
        no return. """
    # read the data thats already there and store it.
    with open('./testsAndResults/output.txt', 'r') as file:
        data = file.readlines()
    # if there's not already an index for the question, make it
    try:
        data[qNumber]
    except IndexError:
        data.append(f'{answer}\n') 
    # for every line already there, 
    for index, line in enumerate(data):
        # check if the question number matches the current question
        if int(line.split(':',1)[0]) == qNumber:
            # if it does, replace it with the new answer.
            data[index] = f'{answer}\n'
    # then open the file in write mode, and write over everything (with the new answer!)
    with open('./testsAndResults/output.txt', 'w') as file:
        file.writelines(data)
    return None

def calculateScoreFromFile():
    """calculates the score from a finished test file. 
    Returns the achieved score and the number of questions in a tuple."""
    sliceobj = slice(-2, -6, -1) # skips the new line characters
    score = 0
    with open('./testsAndResults/output.txt', 'r') as file:
        data = file.readlines()
    for index, line in enumerate(data):
        if line[sliceobj] == 'eurT': # True backwards
            score += 1
    return (score, len(data))

def setupFile(count):
    """sets up an output file for a test. No return."""
    with open('./testsAndResults/output.txt', 'r+') as file:
        file.truncate(0)
        for i in range(count):
            file.writelines(f'{i}:\n')