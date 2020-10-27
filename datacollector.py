import time
import numpy as np
import os 
class DataCollector:
    scores = []
    gameLengths= []
    epsilon = []
    losses = []
    playerx = []
    playery = []
    applex = []
    appley = []
    
    savePath = "data/"+time.strftime("%Y%m%d-%H%M%S")
    def __init__(self):
        #print(self.savePath)
        os.mkdir(self.savePath)
    def add(self,score,length,ep,loss):
        self.scores.append(score)
        self.gameLengths.append(length)
        self.epsilon.append(ep)
        #self.losses.append(mean(loss))

    def record(self,px,py,ax,ay):
        self.playerx.append(px)
        self.playery.append(py)
        self.applex.append(ax)
        self.appley.append(ay)

    def saverecord(self,counter):
        self.playerx = []
        self.playery = []
        self.applex = []
        self.appley = []

    def save(self):
        # s = np.array((self.scores,self.gameLengths,self.epsilon,self.losses))
        s = np.array((self.scores,self.gameLengths,self.epsilon))
        s= np.transpose(s)
        np.savetxt(self.savePath+"/data.csv",s,delimiter=",")
        
