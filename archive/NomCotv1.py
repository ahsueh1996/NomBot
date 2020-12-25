import pyautogui as emu
import time
import datetime as datetime
# from NomTrainer import leftSamples, rightSamples

leftCat = [(642,447), 'left']
rightCat = [(717,447), 'right']

leftSamples = [(611, 488),(608, 485),(609, 481),(616, 479),(623, 479),(629, 481),(635, 486),(640, 489),(643, 494),(640, 500),(633, 506),(627, 509),(614, 510),(601, 510),(604, 504),(611, 491),(618, 502),(630, 493),(632, 501),(648, 499),(639, 514),(626, 519),(613, 515),(608, 502),(615, 488),(618, 482),(607, 492),(615, 499),(624, 482),(640, 477),(645, 495),(615, 485),(630, 469),(640, 484),(614, 473),(634, 459),(625, 470),(626, 456),(639, 464),(645, 454),(642, 466),(647, 489),(619, 495),(617, 461),(634, 455),(627, 449),(635, 439),(638, 433),(636, 444),(617, 438),(631, 451),(632, 434),(643, 421),(657, 438),(640, 457),(619, 452),(633, 427),(614, 423),(622, 442),(607, 445),(593, 442),(604, 455),(601, 486),(604, 492),(610, 454),(607, 427),(607, 424),(624, 429),(609, 442),(634, 452),(634, 463),(607, 475),(640, 480),(650, 497),(658, 504),(636, 499),(657, 458),(664, 436),(651, 477),(651, 499),(614, 492),(607, 501),(642, 503),(651, 512),(653, 494),(667, 459),(658, 438),(670, 475),(669, 492),(678, 470),(667, 483),(641, 487),(650, 442),(621, 427),(626, 463),(610, 485),(639, 500),(606, 504),(607, 470),(627, 446),(633, 478),(650, 462),(651, 440),(654, 432),(632, 469)]
rightSamples = [(721, 494),(732, 488),(737, 487),(749, 485),(756, 485),(748, 489),(726, 498),(717, 507),(717, 510),(722, 513),(739, 512),(752, 502),(753, 493),(753, 499),(739, 505),(721, 507),(710, 514),(717, 497),(730, 494),(721, 485),(708, 491),(696, 480),(697, 479),(701, 467),(716, 473),(729, 482),(743, 467),(749, 480),(744, 476),(714, 458),(721, 459),(712, 447),(703, 445),(715, 437),(748, 467),(747, 491),(747, 496),(750, 499),(755, 500),(755, 491),(754, 456),(754, 449),(753, 437),(753, 437),(752, 434),(742, 434),(723, 434),(719, 434),(706, 434),(706, 434),(720, 448),(730, 450),(742, 449),(740, 465),(722, 441),(695, 439),(688, 439),(706, 467),(721, 463),(718, 429),(699, 420),(716, 422),(718, 434),(712, 435),(730, 437),(729, 433),(746, 434),(718, 442),(730, 478),(693, 489),(716, 495),(722, 506),(719, 495),(714, 470),(708, 452),(736, 456),(741, 474),(746, 494),(700, 463)]

rightHigh = [(708, 447),(723, 444),(747, 442),(770, 442),(788, 442),(805, 442),(819, 442),(825, 442),(835, 436),(836, 433),(835, 425),(830, 423),(791, 423),(766, 423),(739, 423),(722, 415),(719, 406),(728, 401),(766, 404),(804, 404),(827, 404),(830, 396),(826, 394),(809, 388),(751, 392),(703, 394),(689, 382),(711, 373),(711, 358),(729, 366),(744, 366),(778, 392),(809, 356),(828, 380),(842, 361),(804, 359),(739, 351),(699, 343),(710, 332),(774, 338),(814, 340),(826, 362),(734, 351),(729, 347),(765, 352),(788, 347),(831, 354),(830, 361),(827, 380),(795, 374),(748, 361),(714, 382),(769, 386),(755, 405),(760, 428),(816, 423),(788, 445),(794, 397),(788, 379),(750, 425),(727, 437),(767, 395),(749, 440),(726, 453),(722, 447),(745, 449),(815, 458),(830, 441),(818, 445),(805, 467),(740, 463),(718, 443),(745, 456),(777, 449),(843, 434),(763, 434),(752, 406),(796, 404),(744, 416),(719, 384),(761, 395),(829, 404),(743, 404)]
leftHigh = [(668, 468),(655, 472),(619, 472),(594, 472),(569, 472),(536, 473),(532, 473),(517, 465),(515, 446),(545, 448),(600, 450),(663, 451),(664, 452),(627, 446),(542, 446),(509, 436),(517, 416),(565, 418),(604, 419),(645, 415),(670, 406),(664, 399),(608, 398),(551, 407),(519, 401),(514, 386),(517, 373),(579, 369),(606, 370),(648, 374),(660, 372),(670, 370),(670, 362),(624, 353),(576, 350),(547, 350),(524, 350),(515, 368),(576, 358),(639, 357),(665, 353),(677, 363),(674, 382),(644, 356),(568, 357),(524, 362),(520, 366),(537, 375),(593, 373),(602, 373),(631, 380),(647, 377),(570, 381),(537, 394),(592, 400),(575, 408),(608, 383),(617, 425),(569, 419),(592, 426),(633, 424),(577, 437),(601, 449),(591, 419),(573, 401),(608, 415),(532, 424),(520, 453),(516, 463),(549, 472),(616, 467),(663, 471),(660, 462),(612, 464),(604, 466),(590, 434),(652, 432),(592, 435),(644, 406),(654, 423),(607, 406),(539, 426),(587, 379),(649, 380),(627, 372),(558, 364),(569, 349),(605, 372),(545, 383),(601, 402),(574, 428),(625, 441),(593, 417)]

num_samples = min(len(leftSamples),len(rightSamples))
num_high = min(len(leftHigh),len(rightHigh))
bomb = (203,0,0)
fish = (155,155,203)

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

key_state = [1,1]
onThresh = 5
onLag = [onThresh,onThresh]


def mouthDo(l,r):
    cmd, switch = l
    if switch and key_state[0]:
        emu.keyUp(cmd,_pause=False)
        key_state[0] = 0
        onLag[0] = 0
    elif not(switch and key_state[0]):
        if onLag[0] > onThresh:
            emu.keyDown(cmd,_pause=False)
            key_state[0] = 1
        else:
            onLag[0] += 1
    cmd, switch = r
    if switch and key_state[1]:
        emu.keyUp(cmd,_pause=False)
        key_state[1] = 0
        onLag[1] = 0
    elif not(switch and key_state[1]):
        if onLag[1] > onThresh:
            emu.keyDown(cmd,_pause=False)
            key_state[1] = 1
        else:
            onLag[1] += 1        
        
for match in range(int(matches)):
    logging = []
    emu.click(playagain[0][0][0],playagain[0][0][1])
    time.sleep(1)
    emu.click(playagain[0][1][0],playagain[0][1][1])
    time.sleep(1)
    step = 0
    gameOver = False
    
    key_state = [1,1]
    onLag = [1,1]
    
    start = datetime.datetime.now()
    emu.keyDown('left', _pause=False)
    emu.keyDown('right', _pause=False)
    

    
    while not gameOver:
        leftClose = False
        rightClose = False
        leftFish = False
        rightFish = False
        leftSalvo = False
        rightSalvo = False
        
        im = emu.screenshot()#str(match)+'-'+str(step)+'.png')
        for index in range(num_samples):
            if leftClose and rightClose:
                break
            if not leftClose:
                if im.getpixel((leftSamples[index][0],leftSamples[index][1]))[1] < 5:#emu.pixelMatchesColor(leftCat[0][0],leftCat[0][1],bomb):
                    leftClose = True
            if not rightClose:
                if im.getpixel((rightSamples[index][0],rightSamples[index][1]))[1] < 5:#emu.pixelMatchesColor(rightCat[0][0],rightCat[0][1],bomb):
                    rightClose = True
        
#         for index in range(num_high):
#             if leftFish and rightFish and leftSalvo and rightSalvo:
#                 break
#             if not leftSalvo:
#                 if im.getpixel((leftHigh[index][0],leftHigh[index][1]))[1] < 5:#emu.pixelMatchesColor(leftCat[0][0],leftCat[0][1],bomb):
#                     leftSalvo = True
#             if not rightSalvo:
#                 if im.getpixel((rightHigh[index][0],rightHigh[index][1]))[1] < 5:#emu.pixelMatchesColor(rightCat[0][0],rightCat[0][1],bomb):
#                     rightSalvo = True
#             if not leftFish:
#                 test = im.getpixel((leftHigh[index][0],leftHigh[index][1]))
#                 if 149 < test[0] < 158:
#                     if 149 < test[1] < 158:
#                         if 199 < test[2] < 204:
#                             leftFish = True
#             if not rightFish:
#                 test = im.getpixel((rightHigh[index][0],rightHigh[index][1]))
#                 if 149 < test[0] < 158:
#                     if 149 < test[1] < 158:
#                         if 199 < test[2] < 204:
#                             rightFish = True

        mouthDo((leftCat[1],leftClose), (rightCat[1],rightClose))
        
        if step%10 == 9:
            gameOver = emu.pixelMatchesColor(playagain[0][0][0],playagain[0][0][1],playagain[1][0])
            
        step += 1
    
    end = datetime.datetime.now()
    leftClose = True
    rightClose = True
    mouthDo((leftCat[1],leftClose), (rightCat[1],rightClose))
    print('reporting match #'+str(match)+': ')
    for step,each in enumerate(logging):
        print(str(step)+': '+str(each))
    print((end - start)/step)
       
