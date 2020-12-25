import pyautogui as emu
import time

'''
2017 Apr
Albert Hsueh

Helper script that records screen information using py auto gui lib
2 modes:
    0, point to a point you would like to test and hit enter, the color in RGB
        and the xy coord is returned
    1, point to a point you would like to test and hit enter, the xy coord is
        returned. enter r for reset and the previous points sampled will return
        in an array format (ordered oldest to newest). 
    note that this only works for the primary screen.    
'''

mode = input('0-color at point, 1-sampling: ')

while mode == '0':
    input('press enter to display info')
    im = emu.screenshot()
    print(emu.position())
    print('color: '+str(im.getpixel(emu.position())))

samples = []            # store samples in this array
while mode == '1':
    cmd = input('press enter to sample, r to reset: ')
    samples.append(emu.position())
    print(samples[-1])
    
    # when r input is detected, print the sampels in array format
    if cmd == 'r':
        print('\n\n\n')
        s = '['
        for each in samples:
            s = s + str(each) + ','
        s = s[:-1] + ']'
        print(s)
        samples = []
    
