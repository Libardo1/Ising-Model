#!usr/bin/env python
from math import *
import random
from matplotlib import pyplot as plt
import sys
import numpy

def _bin(x, width):
    #converts number x to binary with fixed width, padded by zeroes
    return ''.join(str((x>>i)&1) for i in xrange(width-1,-1,-1))

def partition(stateList,beta):
    current = 0.0
    for state in stateList:
        current += canon(beta,state)
    return current

def canon(beta,state):
    return exp(-beta*Hamiltonian(state))

def Hamiltonian(state):
    current = 0.0
    n = sqrt(len(state))
    listState = []
    for i in state:
        listState.append(int(i))
    array = numpy.array(listState)
    array.resize(n,n)
    counter = 0
    for i in range(n-1):
        for j in range(n-1):
            current += array[i,j] * (array[(i+1 % n),j] + array[(i-1 % n),j] + array[i,(j+1 % n)] + array[i,(j-1 % n)])
    current /= -2
    print array
    return current

def generateStates(n):
    stateList = []
    for i in range(0,2**(n**2)):
        state = _bin(i,n**2)
        stateList.append(state)
    return stateList

def generateMag(stateList,n):
    Mu_Dict = {}
    for state in stateList:
        mu = 0
        for i in state:
            i = int(i)
            if i == 0:
                mu -= 1
            else:
                mu += 1
        mu /= float(n)**2
        if mu in Mu_Dict:
            Mu_Dict[mu] += [state]
        else:
            Mu_Dict[mu] = [state]
    return Mu_Dict

if __name__ == "__main__":
    n = int(sys.argv[1])
    beta = float(sys.argv[2])
    stateList = generateStates(n)
    mu = generateMag(stateList,n)
    Z = partition(stateList,beta)
    x = []
    y = []
    for m in mu:
        for state in mu[m]:
            x.append(m)
            y.append(canon(beta,state)/Z)
    for state in stateList:
        print state
        print Hamiltonian(state)
    #print x,y
    plt.figure()
    plt.plot(x,y)
    plt.show()


    
