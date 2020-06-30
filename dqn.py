## deep q-learning! neural network for reinforcement learning with the snake game
from keras.optimizers import Adam # minimize loss- optimizer
from keras.models import Sequential # sequential neural network model
from keras.layers.core import Dense, Dropout #dense - everything connected to everything, dropout- randomly silence/disconnect some neurons so you don't have overfitting
import random
import numpy as np
import pandas as pd
from operator import add 
import collections

class dqnagent(object):
    def __init__(self,params):
        self.reward = 0 #reward for succeeding/failing the task
        self.gamma = 0.9 #discount rate: how much it weighs rewards in the distant future
        self.dataframe = pd.DataFrame()
        self.short_memory = np.array([]) #buffer for memory?
        self.agent_target = 1
        self.agent_predict = 0
        self.learning_rate = params['learning_rate'] #amount you change your predictions by- size of change you make in direction of descent
        self.epsilon = 1 #rate of exploration vs exploitation- need model to try different states to improve it
        self.actual = []
        self.first_layer = params['first_layer_size']
        self.second_layer = params['second_layer_size']
        self.third_layer = params['third_layer_size']
        self.memory = collections.deque(maxlen=params['memory_size']) #stack/queue effecient storing memory- faster than a list!
        self.weights = params['weights_path'] #weights
        self.load_weights = params['load_weights']
        self.model = self.network ## the network

    def network (self): #building the neural network
        model = Sequential() #layers all in sequential line?
        model.add(Dense(output_dim = self.first_layer, activation='relu', input_dim=11)) #first layer on model, 11 inputs, ReLu activation
        model.add(Dense(output_dim=self.second_layer, activation = 'relu')) #second layer
        model.add(Dense(output_dim = self.third_layer, activation='relu')) #thirdlayer
        model.add(Dense(output_dim = 3, activation='softmax')) # last layer- 3 outputs, softmax activation
        
        opt = Adam(self.learning_rate) #optimization to find minimum loss point
        model.compile(loss='mse',optimizer=opt) #compile model- mean squared error for difference between target and output averaged across different outputs squared
        if self.load_weights: # if you have weights already to load, might as well load them!!
            model.load_weights(self.weights)
        return(model)

    def get_state(self,game,player,food): #returns the diferent states of the player
        state = [
            ## other 3 danger ones

            player.direction == 0, #right
            player.direction == 1, #left
            player.direction == 2, #up
            player.direction == 3, #down

            food.x < player.x, #food is to the left of the player
            food.x > player.x #food is to the right of the player
            food.y < player.y #food is up from the player
            food.y > player.y #food is down from the player 
        ]
        for i in range(len(state)): #convert list to 0s and 1s
            if(state[i]):
                state[i] = 1
            else:
                state[i]=0
            return np.asarray(state)

    def set_reward (self, player, crash): #set the rewards for different actions
        self.reward = 0
        if (crash): #punishment if you crash
            self.reward = -10
            return(self.reward)
        if player.eaten:
            self.reward = 10 #reward if you eat something
        return(self.reward)
    
    def remember(self,state,action,reward,next_state,done): #recording your state, action, reward, next state etc - log of the different gameplay
        self.memory.append((state,action,reward,next_state,done))

    def replay_new(self,memory,batch_size):
        