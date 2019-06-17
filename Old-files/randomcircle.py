import math
import matplotlib.pyplot as plt
import matplotlib.mlab as mlab
import numpy as np
import random
from decimal import *
import operator


#Read file, receiving parameter of file name
def getdata(file):
    #Open file in 'read only mode'
    with open(file, 'r') as data:
        content = data.readlines()
        content = [x.strip() for x in content]

        #Start a list to store every triples
        datalist = []
        x1 = []
        #add each triangle in lists
        for index in range(0, len(content)):
            test = [int(x) for x in content[index].split(' ')]
            datalist.append(test)
            x1.append(test[2])
        datalist = datalist
        
        return datalist, x1


#Generate a random point given points of triangle, as suggested in a Python book
def generatePointsWithinTriangle(pt1, pt2, pt3):
    s, t = sorted([random.random(), random.random()])
    
    return (s * pt1[0] + (t-s)*pt2[0] + (1-t)*pt3[0],
            s * pt1[1] + (t-s)*pt2[1] + (1-t)*pt3[1])

#Useless function, was used to test a certain functionality
def custMax(lamba):
    cpr = lamba[0]
    flag = 0
    for index in range(0, 3):
        if cpr < lamba[index]:
            cpr = lamba[index]
            flag = index

    return flag

#Returning exit proability result of one triangle
def oneDataset( N, data1 ):
    charlie = 0  #hypotense
    delta = 0 #adjacent
    echo = 0 #opposite
    
    for i in range(0, N+1):
        p1 = (0, 0)
        p2 = (data1[0], 0)
        p3 = (0, data1[1])

        ranpoint = generatePointsWithinTriangle(p1, p2, p3)
        angle = random.randrange(0,361,1)
        #generate random moving direction
        angle = random.uniform(0, 360.9)
        #print(angle)
##        print('-> random Point :' + str(ranpoint) )
##        print('-> random angle : ' + str(angle))

        x = ranpoint[0]
        y = ranpoint[1]
        a = data1[0]
        b = data1[1]
        
        lower = math.degrees( math.atan( y / (a - x) ) ) #correct
        upper = math.degrees( math.atan( x / (b - y) ) ) #correct

        #calculate range of exiting charlie side (longest)
        lowRange = 360 - upper
        UpRange = 90 + lower

        #calculate range of angle exiting delta side (adjacent)
        segmentDeltaAng = math.degrees(math.atan( (a-x)/y ) + math.atan(x/y))
        deltaUpper = segmentDeltaAng + UpRange
        
##        print('Range of Charlie ' + str(lowRange) + ' <->' + str(UpRange))
##        print('Delta part Angle range: ' + str(deltaUpper))

        #Add numbers to counter
        if angle > lowRange or angle < UpRange:
            charlie = charlie + 1

        elif UpRange <= angle < deltaUpper:
            delta = delta + 1

        else:
            echo = echo + 1 
   
    charlieF = round( (float(charlie)/N) , 10)
    deltaF = round( ( float(delta)/N ), 10 )
    echoF = round( ( float(echo)/N ) , 10 )
    return (charlieF , deltaF , echoF)

def findMaxMinP():
    #create new list containing exit p of charlie side
    for j in range(0, len(pList) ):
        longsideP.append(pList[j][0])

    #location triangle in .data, returns max point and min point        
    indexOfMax, maxValue = max(enumerate(longsideP), key=operator.itemgetter(1))
    indexOfMin, minValue = min(enumerate(longsideP), key=operator.itemgetter(1))
    
   # print(longsideP)
   #print(indexOfMax);print(maxValue); print(indexOfMin); print(minValue)
    return maxValue, M[indexOfMax], minValue, M[indexOfMin]

def plotgraph():
    #print('\n\nhahaha')
    #print(x1)
    #print(longsideP)
    print('\nPlotting the graph....')

    #plotting exit probability 
    a = np.array(longsideP)
    #scale of x axis
    plt.hist(a, bins = [0.0,0.1,0.2,0.3,0.31,0.32,0.33,0.34,0.35,0.36,0.37,0.38,0.39,0.4,0.41,0.42,0.43,0.44,0.45,0.46,0.47,0.48,0.49,0.5,0.6,0.7,0.8,0.9,1.0], facecolor='navy')
    plt.xlabel('Probability of exiting the longest side')
    plt.ylabel('Frequency')
    plt.title("Histogram showing distribution of exit probability") 
    plt.grid(True)
    plt.savefig("./result.png")
    plt.show()
    

#proving vadlidation on page 3 
def verfication(outputfile):
    correction = 0
    #repeat oneDataset function for 50 times with Large N and take the average
    for k in range (0, 50):
       p = oneDataset(200000, M[0])
       correction = correction + p[0]
       print('finished' + str(k) + 'st/nd/rd/th calculation') 
       #print('finished' + str(k) + 'st/nd/rd/th calculation')        

    print(correction/50)
    writeoutput(outputfile, ('The validated result = ' +str(correction/50))   )

#function of writing results to output.txt
def writeoutput(outputfile, text):
    outputfile.write("%s\n" % text)
    print(text)
    

if __name__ == "__main__":

    output = open("output.txt", "w")
    output = output
    #question1
    file = 'triangle_triples.data'
    M, x1 = getdata(file)
    longsideP = []

    #question2
    N = 1000 #2(a)
    pList = []  #Charlie (Hypoth), delta(bottom), echo(vertical)
    #iterate each item in the data set
    for index in range( 0, len(M)):
        data1 = M[index]
        print(index)
        print(data1)
        p = oneDataset(N ,data1)
        pList.append(p)

    writeoutput( output , "\nResult below shows list of tuples, each tuple represent probability of each trianle triple case")
    writeoutput( output , "\nEach tuple contains three values, they are p of exiting longest side, opposite side and adjacent respectively, As required in 2) on Project4\n These probabilities are shown below\n")
    writeoutput( output , str(pList) )

    #question3
    MaxP, triangle, MinP, minTriangle = findMaxMinP()

    writeoutput( output , ('\nGreatest probability is '+ str(MaxP)) )
    writeoutput( output , ('The Trangle is '+ str(triangle) ) )         
    writeoutput( output , ('\nSmallest probability is '+ str(MinP)) )
    writeoutput( output , ('The Trangle is '+ str(minTriangle) ) ) 

    writeoutput( output, '\nMy result find that (23,264,265) tend to be the greatest, (119,120,169) or (133, 156, 205)tend to be the smallest, with N increased up to 500000, which is consistant with the value' )

    writeoutput( output, '\nNow proving equation (1) on page3, it might take a while, shortly after that we will plot the graph' )
    
    ##Veriying equation 1 on page3
    verfication( output )
    #closing file
    output.close()
    #plotting graph
    plotgraph()

   