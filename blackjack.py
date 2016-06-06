import pywikibot
from pywikibot import pagegenerators
import json

site = pywikibot.Site('en', 'metakgp')

def load(file):  #convert to string json
    def convert(input):
        if isinstance(input, dict):
            return {convert(key): convert(value) for key, value in input.iteritems()}
        elif isinstance(input, list):
            return [convert(element) for element in input]
        elif isinstance(input, unicode):
            return input.encode('utf-8')
        else:
            return input

    dict_unicode = json.loads(open(file).read())
    return convert(dict_unicode)


def retreivePage(courseCode):
    tempGen = pagegenerators.SearchPageGenerator(courseCode, namespaces=[0])
    tempList = []
    for i in tempGen:
        tempList.append(i)
    if(len(tempList) != 0):
        return tempList[0]
    else:
        return False

def genGraph(courseCode):
    stats = allCourses[courseCode]
    text = u'\n| grades = {{Grades\n'+ ' '*11 +'| EX = '+ str(stats['EX']) +'\n'+ ' '*11 +'| A = '+ str(stats['A']) +'\n'+ ' '*11 +'| B = '+ str(stats['B']) +'\n'+ ' '*11 +'| C = '+ str(stats['C']) +'\n'+ ' '*11 +'| D = '+ str(stats['D']) +'\n'+ ' '*11 +'| P = '+ str(stats['P']) +'\n'+ ' '*11 +'| F = '+ str(stats['F']) +'\n'+ ' '*11 +'}}\n'
    return text

def getValidCodes():
    for i in allCourses:
        if(retreivePage(i)):
            validCodes.append(i)
            
def getNullCodes():
    for i in allCourses:
        if not retreivePage(i):
            nullCodes.append(i)

def insertBefore(data, pattern, newText):
    i = data.find(pattern)
    return data[:i] + newText + data[i:]

def genPageNewText(courseCode):
    return insertBefore(retreivePage(courseCode).text,'\n}}',genGraph(courseCode))

def updatePage(courseCode):
    temp = retreivePage(courseCode)
    temp.text = genPageNewText(courseCode)
    temp.save(summary='Added previous year\'s grade distribution',botflag=True, callback = caller)

def caller(page,err):
    if not err:
        savedPages.append(page)
    else:
        print err, 'occured'

allCourses = load('./allCourses.json')  

validCodes = []
nullCodes = []
savedPages=[]

getValidCodes()

for i in validCodes:
    updatePage(i)