import pyautogui as emu
import time
import datetime as datetime

leftCat = [(607,440), 'left']
rightCat = [(753,440), 'right']
searchRegion = (10,5)
bomb = (203,0,0)

playagain = [[(679,684),(679,398)],
             [(64,128,255),(64,128,255)]]
matches = input('Enter number of matches to start: ')
print('3')
time.sleep(1)
print('2')
time.sleep(1)
print('1')
time.sleep(1)
print('start!')

def mouthDo(l,r):
    cmd, switch = l
    output = [0,0]
    if switch:
        emu.keyUp(cmd)
    else:
        emu.keyDown(cmd)
        output[0] = 1
    cmd, switch = r
    if switch:
        emu.keyUp(cmd)
    else:
        emu.keyDown(cmd)
        output[1] = 1
    print(datetime.datetime.now())
    print(output)
                
for match in range(int(matches)):
    emu.click(playagain[0][0][0],playagain[0][0][1])
    time.sleep(1)
    emu.click(playagain[0][1][0],playagain[0][1][1])
    time.sleep(1)
    step = 0
    
    while not emu.pixelMatchesColor(playagain[0][0][0],playagain[0][0][1],playagain[1][0]):
        step += 1
        leftClose = False
        rightClose = False
        mouthDo((leftCat[1],leftClose), (rightCat[1],rightClose))
        print(step)
        
        im = emu.screenshot(str(match)+'-'+str(step)+'.png')
        
        for test in range(-searchRegion[0],searchRegion[0],searchRegion[1]):
            if leftClose and rightClose:
                break
            if not leftClose:
                if emu.pixelMatchesColor(leftCat[0][0]+test,leftCat[0][1],bomb):#im.getpixel((leftCat[0][0]+test,leftCat[0][1])) == bomb:#
                    print('left BOMB')
                    leftClose = True
            if not rightClose:
                if emu.pixelMatchesColor(rightCat[0][0]+test,rightCat[0][1],bomb):#im.getpixel((rightCat[0][0]+test,rightCat[0][1])) == bomb:#
                    print('right BOMB')
                    rightClose = True
       
        mouthDo((leftCat[1],leftClose), (rightCat[1],rightClose))
#         time.sleep(.1)
    
    print('death...')
    leftClose = True
    rightClose = True
    mouthDo((leftCat[1],leftClose), (rightCat[1],rightClose))       