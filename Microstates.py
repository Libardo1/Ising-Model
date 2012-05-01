#!usr/bin/env python
# Ising model probability generator for states in a 2 dimensional n x n spin system
from math import *
import random
from matplotlib import pyplot as plt
import sys
import numpy

def _bin(x, width):
    #converts number x to binary with fixed width, padded by zeroes
    return ''.join(str((x>>i)&1) for i in xrange(width-1,-1,-1))

def partition(stateList,beta,n):
    #calculates partition function Z for all states in stateList with given temp of 1/beta
    current = 0.0
    for state in stateList:
        current += canon(beta,state,n)
    return current

def canon(beta,state,n):
    #calculates canonical density for given state at temperature 1/beta
    return exp(-beta*Hamiltonian(state,n))

def Hamiltonian(state,n):
    #calculates the Ising model Hamiltonian
    current = 0.0
    listState = []
    for i in state:
        listState.append(int(i))
    array = numpy.array(listState)
    array.resize(n,n)
    for i in range(n-1):
        for j in range(n-1):
            current += array[i,j] * (array[(i+1 % n),j] + array[(i-1 % n),j] + array[i,(j+1 % n)] + array[i,(j-1 % n)])
    current /= -2
    return current

def generateStates(n):
    stateList = []
    for i in range(0,2**(n**2)):
        state = _bin(i,n**2)
        stateList.append(state)
    return stateList

def generateMag(stateList,n):
    #calculates the total magnetism of all the states, returns in dictionary form
    Mu_Dict = {}
    State_Dict = {}
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
        if state in State_Dict:
            State_Dict[state] += [mu]
        else:
            State_Dict[state] = [mu]
    return Mu_Dict,State_Dict

if __name__ == "__main__":
    n = int(sys.argv[1])
    beta = float(sys.argv[2])
    stateList = generateStates(n)
    muDict = generateMag(stateList,n)[0]
    stateDict = generateMag(stateList,n)[1]
    Z = partition(stateList,beta,n)
    x= [] 
    y = []
    for state in stateDict:
        x.append(stateDict[state])
        y.append(canon(beta,state,n)/Z)
    # y is the list of probabilities for states in x
    plt.hist(x,bins=len(muDict.keys()),weights = y,normed=True)
    plt.show()


    
