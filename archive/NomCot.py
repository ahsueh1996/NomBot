import pyautogui as emu
import time
import datetime as datetime
import numpy as np

w = lambda abcd: abcd[1][0]-abcd[0][0]
h = lambda abcd: abcd[1][1]-abcd[0][1]
c = lambda abcd: (int(w(abcd)/2+abcd[0][0]),int(h(abcd)/2+abcd[0][1]))

refStage = ((508,103),(858,725))   # top left, bottom right

''' define this'''
curStage = ((173, 122),(510, 721))
''''''

scale = (w(curStage)/w(refStage),h(curStage)/h(refStage))
refCent = c(refStage)
curCent = c(curStage)

refZone = [(604, 489),(626, 494),(646, 508),(609, 469),(632, 478),(647, 487),(664, 474),(639, 461),(622, 452),(613, 445),(612, 429),(634, 429),(659, 435),(671, 448),(680, 455),(697, 442),(688, 431),(674, 419),(655, 412),(640, 408),(622, 400),(634, 382),(657, 390),(673, 394),(697, 409),(709, 418),(721, 431),(733, 429),(716, 412),(695, 391),(667, 370),(637, 362),(650, 349),(678, 361),(696, 371),(719, 385),(729, 400),(751, 415),(764, 423),(778, 414),(768, 396),(747, 378),(731, 368),(710, 352),(695, 341),(669, 333),(692, 311),(715, 321),(742, 341),(765, 360),(782, 374),(801, 389),(816, 408),(838, 408),(823, 390),(808, 364),(788, 339),(768, 329),(743, 316),(724, 305),(698, 284),(706, 263),(731, 269),(757, 287),(783, 312),(808, 328),(829, 351),(850, 368),(851, 342),(834, 313),(821, 295),(802, 276),(785, 259),(774, 251),(753, 235),(787, 225),(808, 244),(834, 273),(853, 302),(852, 275),(836, 250),(821, 223),(811, 209),(841, 210),(849, 234)]+[(651, 394),(661, 371),(678, 342),(698, 312),(673, 298),(645, 325),(627, 351),(615, 383),(590, 381),(605, 337),(628, 303),(662, 268)]


leftZone = [((p[0]-refCent[0])*scale[0]+curCent[0],
             (p[1]-refCent[1])*scale[1]+curCent[1]) for p in refZone]
rightZone = [((p[0]-curCent[0])*-1+curCent[0],p[1]) for p in leftZone]

bomb = [(203,0,0),(131, 0, 0),(61, 91, 92),(223, 223, 223),(255, 235, 144)]
fish = [(155,155,203),(157, 157, 204),(154, 154, 202),(137, 137, 194),(46, 55, 97),(115, 115, 183),(119, 119, 187),(111, 111, 180)]

a = (679-refCent[0])*scale[0]+curCent[0]
playagain = [[(a,(684-refCent[1])*scale[1]+curCent[1]),(a,(398-refCent[1])*scale[1]+curCent[1])],
             [(64,128,255),(64,128,255)]]

class Cat():
    def __init__(self,control,zone,histSize,weights):
        self.control = control
        self.zone = zone
        self.harvestHistory = [[0]*len(zone)]*histSize
        self.weights = weights
        self.cmd = 0
        
    def act(self):
        if self.cmd>=1:
            emu.keyDown(self.control,_pause=False)
        elif self.cmd<=-1:
            emu.keyUp(self.control,_pause=False)
    
    def plan(self,im):
        self.harvestHistory.pop()
        self.harvestHistory.append(self.harvest(im))
        self.cmd = round(np.sum(np.dot(np.array(self.harvestHistory),np.array(self.weights).T)))
    
    def harvest(self,im):
        array = []
        for p in self.zone:
            pixel = im.getpixel((p[0],p[1]))
            if pixel in bomb:
                array.append(-1.)
            elif pixel in fish:
                array.append(1.)
            else:
                array.append(0.01)
        return array
    
    def no_action(self):
        emu.keyUp(self.control,_pause=False)

def play(leftCat, rightCat,matches=None):
    if matches == None:
        matches = input('Enter number of matches to start: ')
        for count in range(3):    
            print(str(3-count))
            time.sleep(1.5)
        print('start!')
    
    matchRecords = []
      
    for match in range(int(matches)):
        logging = []
        step = 0
        gameOver = False
        
        emu.click(playagain[0][0][0],playagain[0][0][1])
        time.sleep(1)
        emu.click(playagain[0][1][0],playagain[0][1][1])
        time.sleep(1)

        start = datetime.datetime.now()
    
        while not gameOver:
            im = emu.screenshot()#str(match)+'-'+str(step)+'.png')
            leftCat.plan(im)
            rightCat.plan(im)
            leftCat.act()
            rightCat.act()
            if step%5 == 4:
                gameOver = emu.pixelMatchesColor(playagain[0][0][0],playagain[0][0][1],playagain[1][0])
            step += 1
        
        end = datetime.datetime.now()
        leftCat.no_action()
        rightCat.no_action()
#         print('reporting match #'+str(match)+': ')
#         for step,each in enumerate(logging):
#             print(str(step)+': '+str(each))
#         print((end - start)/step)
        matchRecords.append(step)
    return matchRecords
       
