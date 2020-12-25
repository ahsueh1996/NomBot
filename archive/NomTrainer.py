import NomCot
import numpy as np
import pickle
import os
import random


''' define these settings '''
attrSize = len(NomCot.refZone)
histSize = 3
num_offsprings = 15
matches = 3
filename = 'nomCot-NN-2'
''''''


''' weights will look like:
 [ [.... weights for one history...],
    [.... weights for another......],
    .           .            .      ]
'''

def mate(champions,num_offsprings):
    ''' input 2 champions' weights and the number of offsprings
    to generate. Offsprings will obviously have the same size weights'''
    histSize, attrSize = np.shape(champions[0])
    offsprings = [[[0]*attrSize]*histSize]*num_offsprings
    
    for i in range(histSize):
        for j in range(attrSize):
            a = champions[0][i][j]
            b = champions[1][i][j]
            for k in range(num_offsprings):
                offsprings[k][i][j] = mutate(a,b)
                
    return offsprings+champions

def mutate(a,b):
    mean = (a+b)/2
    variance = max((abs(a-b)/2)**2,max(0.01,(random.random()+.02)**32))
    return np.random.normal(mean,variance)

''' ################### Main trainer starts #########################'''

if not (filename+'-refZone.pkl' in os.listdir()):
    with open(filename+'-refZone.pkl','wb') as file:
        pickle.dump(NomCot.refZone,file)

if filename+'-weights.pkl' in os.listdir():
    print('weights found, loading...')
    with open(filename+'-weights.pkl','rb') as file:
        data = pickle.load(file)
    champions = data['champs']
    evolution = data['evol'] 
else:
    champions = [ [[np.random.normal(0,0.1) for i in range(attrSize)] for j in range(histSize)],
                [[np.random.normal(0,0.1) for i in range(attrSize)] for j in range(histSize)] ]
    evolution = 1

offsprings = mate(champions, num_offsprings)

while True:
    print('generation '+str(evolution)+': =======================')
    results = []
    for offspring in offsprings:
        res = NomCot.play(NomCot.Cat('left',NomCot.leftZone,histSize,offspring),
                    NomCot.Cat('right',NomCot.rightZone,histSize,offspring), matches)
        results.append(sum(res)/len(res))
        print('max: %d, avg: %f' % (max(res),sum(res)/len(res)))
    placing = np.argsort(results)[::-1]
    print(placing)
    if (results[placing[0]]-results[placing[1]])/results[placing[0]]>.87:
        champions = [offsprings[placing[0]],offsprings[placing[0]]]
    else:
        champions = [offsprings[placing[0]],offsprings[placing[1]]]
    with open(filename+'-weights.pkl','wb') as file:
        pickle.dump({'champs':champions,'evol':evolution},file)
    evolution += 1
    print('==================: '+str(sum(results)/len(results)))
    


