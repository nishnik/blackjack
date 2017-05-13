from subprocess import check_output
import re
import json
import progressbar
import urllib2

def load(file):
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

def save(dic, name):
    with open(name + ".json", "w") as outfile:
        json.dump(dic, outfile)
        
cookie = '43E3828C7782BC1EDD306A57DF7FA26F.worker3'

opener = urllib2.build_opener()
opener.addheaders.append(('Cookie', 'JSESSIONID={}'.format(cookie)))
        
def getGrades(code):
    f = opener.open("https://erp.iitkgp.ernet.in/Acad/Pre_Registration/subject_grade_status.jsp?subno={}".format(code))
    nums = re.findall('([A-Z\s]+)\(No. of Student\) : ([0-9]+)', f.read())
    if len(nums)!=0:
        return {str(d[0].strip()): int(d[1]) for d in nums}
    else:
        return {}
    
def uniformizeGradesJSON(stats):
    for i in ['EX','A','B','C','D','P','F']:
        if i not in stats:
            stats[i] = 0
    return stats
    
def main():
    newGrades = {}
    allcourses = load('courses.json').keys()
    with progressbar.ProgressBar(max_value=len(allcourses)) as bar:
        for n, i in enumerate(allcourses):
            while True:
                try:
                    g = getGrades(i);
                    if len(g)!=0:
                        newGrades[i] = {'grades': uniformizeGradesJSON(g)}
                        print i, newGrades[i]
                except Exception as e:
                    print i, e
                break
            bar.update(n)

    save(newGrades, 'newGrades')

if __name__ == '__main__':
    main()
