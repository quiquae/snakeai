from pygame.locals import *
from random import random, randint
import pygame
import os
import time
import numpy as np

from dqn2 import dqnagent
from apple import Apple
from player import Player
from game import Game
from datacollector import DataCollector
from toolbar import Toolbar

def parameters():
    params = dict()
    params['epsilon_decay_linear'] = 1/75 #how much we decrease our exploration by every time
    params['learning_rate'] = 0.0005
    params['first_layer_size'] = 150 #size(nodes) of neural network layer 1
    params['second_layer_size'] = 150
    params['third_layer_size'] = 150
    params['episodes'] = 15 #how many trials you do ie played games
    params['memory_size'] = 2500
    params['batch_size'] = 500
    params['weights_path_save'] = 'weights/'+time.strftime("%Y%m%d-%H%M%S") #file path for the weights folder
    params['weights_path_load'] = 'weights/weights.hdf5'
    params['load_weights'] = False
    params['train'] = True
    return(params)
    
class App:
    windowDimY = 14
    windowDimX = 18
    windowWidth = 0
    windowHeight = 0
    toolbarWidth = 200
    player = 0
    apple = 0
    toolbar = 0
    dataCollect = 0
    displayq = False
 
    def __init__(self,dq,state,freq):
        self._running = True
        self._display_surf = None
        self._image_surf = None
        self._apple_surf = None

        self.game = Game()
        self.player = Player(3,self.windowDimX, self.windowDimY)
        self.windowWidth = self.windowDimX*self.player.step
        self.windowHeight = self.windowDimY*self.player.step 
        self.toolbar = Toolbar(self.toolbarWidth, self.windowWidth, self.windowHeight)
        self.apple = Apple(randint(0,self.windowDimX-1), randint(0,self.windowDimY-1))
        self.dataCollect = DataCollector()
        self.displayq=dq
        self.state_size = state
        self.frequency = freq

    def on_init(self):
        pygame.init()
        if(self.displayq):
            self._display_surf = pygame.display.set_mode((self.windowWidth+self.toolbarWidth,self.windowHeight), pygame.HWSURFACE)
            pygame.display.set_caption('Pygame Snake game!')
            self._image_surf = pygame.image.load("images/game_objects/smake.png").convert()
            self._apple_surf = pygame.image.load("images/game_objects/smapple.png").convert()
            self.toolbar.load_images()
        self._running = True
        # self.savepath = "frames/"+time.strftime("%Y%m%d-%H%M%S")
        # os.mkdir(self.savepath)
 
    def on_event(self, event):
        if event.type == QUIT:
            self._running = False
 
    def on_loop(self): 
        self.player.update()

        # does snake collide with itself?
        for i in range(2,self.player.length):
            if self.game.isCollision(self.player.x[0],self.player.y[0],self.player.x[i], self.player.y[i],self.player.step-1):
                print("You lose! Collision with yourself: ")
                print("x[0] (" + str(self.player.x[0]) + "," + str(self.player.y[0]) + ")")
                print("x[" + str(i) + "] (" + str(self.player.x[i]) + "," + str(self.player.y[i]) + ")")
                self.player.crashed = True
                
        # does snake eat apple?
        for i in range(0,self.player.length):
            if self.game.isCollision(self.apple.x,self.apple.y,self.player.x[i], self.player.y[i],self.player.step-1):
                self.apple.x = randint(0,self.windowDimX-1) * self.player.step
                self.apple.y = randint(0,self.windowDimY-1) * self.player.step
                print("apple x=",self.apple.x,"apple y=",self.apple.y)
                self.player.eatenApple = True
 
        #does snake collide with wall?
        if(self.player.x[0]<0 or self.player.x[0]>=self.windowWidth or self.player.y[0]<0 or self.player.y[0]>=self.windowHeight):
            print("You lose! Collision with wall: ")
            print("x[0] (" + str(self.player.x[0]) + "," + str(self.player.y[0]) + ")")
            self.player.crashed = True
        
        pass

    def on_render(self, state):
        self._display_surf.fill((0,0,0))
        self.player.draw(self._display_surf, self._image_surf)
        self.apple.draw(self._display_surf, self._apple_surf)
        self.toolbar.draw(self._display_surf, self.player.direction, state)
        pygame.display.flip()
 
    def on_cleanup(self):
        pygame.quit()

    # initializing agent before the 1st move
    def init_agent(self, agent):
        state_init1 = agent.get_state(game, self.player, self.food) #first state after random placement
        #first action
        
    def reset_player(self):
        self.player = Player(3,self.windowDimX, self.windowDimY)
        #print(self.player.x)
        #print(self.player.y)

    def on_execute(self,speed):
        print('starting execution!')
        params = parameters()
        agent = dqnagent(params,self.state_size) #initialize the agent!
        if(agent.load_weights): #load weights maybe
            agent.model.load_weights(agent.weights)
            print("loaded the weights")

        counter = 0 #how many games have been played/trials done
        record = 0 #highest score

        #---------------------------------------------------------------------------
        #------------------------- LOOP THRU EPISODES ------------------------------
        #---------------------------------------------------------------------------

        while counter<params['episodes']: #still have more trials to do
            counter += 1
            print(counter)

            print("\nEPISODE ", counter, "\n")

            if not params['train']: # if you're not training it, no need for exploration
                agent.epsilon = 0
            else:
                agent.epsilon = 1.0 - ((counter -1) * params['epsilon_decay_linear'])#exploration/randomness factor that decreases over time

            #print("EPSILON = ", agent.epsilon, "\n")

            if self.on_init() == False:
                self._running = False

            #print("PLAYER\tx : ", self.player.x,"\ty : ", self.player.y, "\n")
            duration = 0

            #---------------------------------------------------------------------------
            #--------------------------- INDIVIDUAL EPISODE ----------------------------
            #---------------------------------------------------------------------------
            # indexx = 0
            while(self._running):
                if(counter%self.frequency==0):
                    self.dataCollect.record(self.player.x, self.player.y, self.apple.x, self.apple.y)
                duration+=1
                #print("\nMOVE : ", duration, "\n")
                if(self.displayq):
                    pygame.event.pump()
                    keys = pygame.key.get_pressed() 
                    if (keys[K_ESCAPE]):
                        exit(0)
                oldstate = agent.get_state(self, self.player, self.apple)
                #print("\noldstate = ", oldstate)


                #--------------------------- GET AGENT ACTION ----------------------------

                if random() < agent.epsilon: #every so often random exploration
                    action = randint(0,3) #random action
                    #print("random action : ",action)
                else: #Actionprecited by agent
                    state = oldstate.reshape(1,self.state_size**2+8)
                    predictedq= agent.model.predict(state) # predicts the q values for the action in that state
                    action = np.argmax(predictedq[0]) #maximum (highest q) action
                    #print("predicted action : ", action, "\tq-values : ", predictedq)


                #---------------------------- EXECUTE ACTION -----------------------------

                print(action)
                self.player.do_move(action) #do the action
                self.on_loop()
                newstate = agent.get_state(self, self.player, self.apple) #new state from the action we've taken
                reward = agent.set_reward(self.player)
                #print("newstate = ", newstate)
                #print("reward = ", reward)
                #print("crashed = ", self.player.crashed, "\n")


                #---------------------------- SHORT TRAINING -----------------------------

                if(params['train']):
                    agent.train_short_memory(oldstate,action, reward, newstate, self.player.crashed)
                    agent.remember(oldstate,action, reward, newstate, self.player.crashed)


                #------------------------------ RENDER GAME ------------------------------

                self._running = not(self.player.crashed)
                if(self.displayq):
                    self.on_render(newstate)
                # if(counter%self.frequency==0):
                #     self.on_render(newstate)
                #     pygame.image.save(self._display_surf,savepath+str(indexx))
                time.sleep (speed/1000.0)
                # indexx +=1


            #---------------------------------------------------------------------------
            #----------------------- TRAINING & DATA COLLECTION ------------------------
            #--------------------------------------------------------------------------- 

            if(params['train']):
                agent.replay_new(agent.memory, params['batch_size'])
            
            
            # self.dataCollect.add(self.player.length,duration,agent.epsilon,agent.history.losses)
            self.dataCollect.add(self.player.length,duration,agent.epsilon, 0.0)
            self.dataCollect.save()
            #print(agent.history.losses.length())
            #agent.history.losses = []
            self.player.reset(3,self.windowDimX, self.windowDimY )
            self.on_cleanup()

        #---------------------------------------------------------------------------
        #------------------------------ DATA OUTPUT --------------------------------
        #--------------------------------------------------------------------------- 
        if(params['train']):
             os.mkdir(params['weights_path_save'])
             agent.model.save_weights(params['weights_path_save']+'/weights.hdf5')
        self.dataCollect.save()