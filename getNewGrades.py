from subprocess import check_output
import re
import json
import progressbar
import threading
import urllib2

cookie = '960B1D13D77A203857659227421093F6.worker2'
NUM_THREADS = 1

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

n = 0
def main():
    newGrades = {}
    allcourses = load('courses.json').keys()
    bar = progressbar.ProgressBar(max_value=len(allcourses))
    class ScrapingThread(threading.Thread): # Call it Iron-Man thread
        def __init__(self,courses):
            super(ScrapingThread, self).__init__()
            self.courses=courses
        def run(self):
            global n
            for i in self.courses:
                g = getGrades(i)
                if len(g)!=0:
                    newGrades[i] = {'grades': uniformizeGradesJSON(g)}
                    print i, newGrades[i]
                n += 1
                bar.update(n)
    threads = []
    one_part_len = len(allcourses)/NUM_THREADS
    for i in range(NUM_THREADS):
        threads.append(ScrapingThread(allcourses[i * one_part_len : (i+1) * one_part_len]))
    for i in threads:
        i.start()
    for i in threads:
        i.join()

    for i in newGrades:
        newGrades[i]['grades'].pop('X',None)
        
    save(newGrades, 'newGrades')

if __name__ == '__main__':
    main()
