from Tkinter import *
import urllib2
from xml.dom.minidom import parseString
from xml.dom import *
import time
from collections import defaultdict

master = Tk()

masterSet = defaultdict(lambda: None)
maxCount = 0 

def submit():
    usernames = parse(inputText.get('1.0', 'end'))
    currentUser = getUserShows(user.get())
    userHandler(usernames, currentUser)

    final = generateFinal()

    outputText.delete('1.0', 'end')
    outputText.insert('1.0',final)

def export():
    text_file = open("MALdump.txt", "w")
    text_file.write(outputText.get('1.0', 'end').encode("UTF-8"))
    text_file.close()

def generateFinal():
    global masterSet
    listF = []
    stringF = "NAME|AVG|WEIGHTED|COUNT|ID\n"
    for key, value in masterSet.iteritems():
        temp = [key]+value
        listF.append(temp)
    for entry in listF:  #for now I'm keeping the new copy of the list as well in case I want to do more with it (probably proper text printing).
        i = finalHelper(entry)
        stringF += i[0] + "|" + str(i[1]) + "|" + str(i[2]) + "|" + str(i[3]) + "|" + "https://myanimelist.net/anime/" + i[4] + "\n"
    return stringF

def finalHelper(inL): #converts input list inL to final list of return data
    global maxCount
    factor = 0.866
    return [inL[0], 1.0*inL[1]/inL[2], factor*inL[1]/inL[2] + (1.0 * inL[2] / maxCount) * (1.0 - factor) * 10.0, inL[2], inL[3]]

def userHandler(users, alreadySeen):
    for user in users:
        getInfo(user[0],alreadySeen)
        print user
        #time.sleep(.25)

def getUserShows(username): #checks if username specified; if one is, then all shows not PTW are added to an alreadyseen set.
    if username == "Opt: username" or username == "":
        return []
    seen = []
    dump = urllib2.urlopen("https://myanimelist.net/malappinfo.php?u="+username+"&status=all&type=anime").read()
    animeList = parseString(dump).getElementsByTagName("anime")
    for i in animeList:
        if int(i.getElementsByTagName("my_status")[0].firstChild.data) == 6:
            continue
        seen.append(i.getElementsByTagName("series_title")[0].firstChild.data)
    return seen

#I only did this as a personal challenge to use as many lambdas as possible in a single line. Don't replicate this.
#Parses out usernames and affinities from text dump input.
def parse(inputDump):
    return filter(lambda x: x[0]!= "UserName",[[item[1], item[3]] for item in filter(lambda x: len(x)>1, map(lambda x: x.split('	'),inputDump.split('\n')))])

#Gets xml dump of param username. Loops through every valid listing (valid if not PTW, score not 0 and show not already seen) and then adds them to the master hash map.
def getInfo(username, alreadySeen):
    global maxCount
    dump = urllib2.urlopen("https://myanimelist.net/malappinfo.php?u="+username+"&status=all&type=anime").read()
    animeList = parseString(dump).getElementsByTagName("anime")
    for i in animeList:
        if int(i.getElementsByTagName("my_status")[0].firstChild.data) == 6 or i.getElementsByTagName("series_title")[0].firstChild.data in alreadySeen or int(i.getElementsByTagName("my_score")[0].firstChild.data) == 0:
            continue
        if masterSet[i.getElementsByTagName("series_title")[0].firstChild.data] == None:
            masterSet[i.getElementsByTagName("series_title")[0].firstChild.data] = [int(i.getElementsByTagName("my_score")[0].firstChild.data),1,i.getElementsByTagName("series_animedb_id")[0].firstChild.data]
        else:
            masterSet[i.getElementsByTagName("series_title")[0].firstChild.data][0] += int(i.getElementsByTagName("my_score")[0].firstChild.data)
            masterSet[i.getElementsByTagName("series_title")[0].firstChild.data][1] += 1
        if masterSet[i.getElementsByTagName("series_title")[0].firstChild.data][1] > maxCount:
            maxCount = masterSet[i.getElementsByTagName("series_title")[0].firstChild.data][1]

#tkinter garbage

frame = Frame(master)
frame.grid(row = 0, column = 1, sticky = E+N)

inputText = Text(master, width = 100, height = 20)
inputText.grid(row = 0, column = 0)

outputText = Text(master, width = 100, height = 20)
outputText.grid(row = 1, column = 0)

user = Entry(frame, width=15)
user.grid(row = 0, column = 0,sticky=W+N, padx=5, pady=5)
user.insert(0, "Opt: username")

submitButton = Button(frame, text="Submit", width=15, command=submit)
submitButton.grid(row = 1, column = 0,sticky=E+N, padx=5, pady=5)

exportButton = Button(frame, text="Export", width=15, command=export)
exportButton.grid(row = 2, column = 0,sticky=E+N, padx=5, pady=5)

mainloop()
