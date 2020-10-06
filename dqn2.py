## deep q-learning! neural network for reinforcement learning with the snake game
from keras.optimizers import Adam # minimize loss- optimizer
from keras.models import Sequential # sequential neural network model
from keras.layers.core import Dense, Dropout #dense - everything connected to everything, dropout- randomly silence/disconnect some neurons so you don't have overfitting
import random
import numpy as np
import pandas as pd
from operator import add 
import collections
from keras.callbacks import Callback

class lossHistory(Callback):
    def on_train_begin(self,logs = {}):
        self.losses = []
    def on_batch_end(self,batch,logs={}):
        self.losses.append(logs.get('loss'))

class dqnagent(object):
    def __init__(self,params,state_Size):
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
        self.weights = params['weights_path_load'] #weights
        self.load_weights = params['load_weights']
        self.dim = state_Size
        self.model = self.network() ## the network
        self.history = lossHistory()
    

    def network (self): #building the neural network
        model = Sequential() #layers all in sequential line?
        model.add(Dense(units = self.first_layer, activation='relu', input_dim=(self.dim**2+8))) #first layer on model, 33 inputs, ReLu activation
        model.add(Dense(units=self.second_layer, activation = 'relu')) #second layer
        model.add(Dense(units = self.third_layer, activation='relu')) #thirdlayer
        model.add(Dense(units = 4, activation='softmax')) # last layer- 3 outputs, softmax activation
        
        opt = Adam(self.learning_rate) #optimization to find minimum loss point
        model.compile(loss='mse',optimizer=opt) #compile model- mean squared error for difference between target and output averaged across different outputs squared
        if self.load_weights: # if you have weights already to load, might as well load them!!
            model.load_weights(self.weights)
        return(model)

    def get_state(self,app,player,food): #returns the diferent states of the player
        middle = int(self.dim/2)
        grid = np.zeros((self.dim,self.dim),dtype=bool)
        print("x=",player.x,"y=",player.y)
        relativex = [int((a-player.x[0])/player.step+middle) for a in player.x]
        relativey = [int((a-player.y[0])/player.step+middle) for a in player.y]
        for x,y in zip(relativex, relativey):
            if(x>=0 and y>=0 and x<self.dim and y<self.dim):
                grid[y,x]= True

        right = int(app.windowDimX-(player.x[0]/player.step)+middle)
        down = int(app.windowDimY-(player.y[0]/player.step)+middle)
        up = int(middle-(player.y[0]/player.step))
        left = int(middle-(player.x[0]/player.step))
        if(right<self.dim and right>=0):
            grid[:,right:] = True
        if(left<self.dim and left>=0):
            grid[:,:left] = True
        if(down<self.dim and down>=0):
            grid[down:,:] = True
        if(up<self.dim and up>=0):
            grid[:up,:] = True

        grid = list(grid.flatten())

        state = [

            player.direction == 0, #right
            player.direction == 1, #left
            player.direction == 2, #up
            player.direction == 3, #down

            food.y < player.y[0], #food is up from the player
            food.y > player.y[0], #food is down from the player
            food.x < player.x[0], #food is to the left of the player
            food.x > player.x[0] #food is to the right of the player
             
        ]
        state += grid
        for i in range(len(state)): #convert list to 0s and 1s
            if(state[i]):
                state[i] = 1
            else:
                state[i]=0

        return np.asarray(state)

    def set_reward (self, player): #set the rewards for different actions
        self.reward = 0
        if (player.crashed): #punishment if you crash
            self.reward = -10
            return(self.reward)
        if player.eatenApple:
            self.reward = 10 #reward if you eat something
        return(self.reward)
    
    def remember(self,state,action,reward,next_state,done): #recording your state, action, reward, next state etc - log of the different gameplay
        self.memory.append((state,action,reward,next_state,done))

    def replay_new(self,memory,batch_size): #replaying small chunks of the game history to train the model
        if len(memory) > batch_size: #more memory than size of bath
            minibatch = random.sample (memory, batch_size) #small randomly sampled batch
        else:
            minibatch = memory #batch too big so gets all of the memory
        for state, action, reward, next_state, done in minibatch: 

            #print("\n\nprev state: ", state, "\naction: ", action, "\nreward: ", reward, "\nnext state: ", next_state, "\ncrashed: ", done)

            target = reward #target is the estimation of the correct q-value
            # sets the target equal to reward or estimation of what that is if game isn't finished
            if not done:
                target = reward + self.gamma * np.amax(self.model.predict(np.array([next_state]))[0])
            
            #print("target: ", target)
            target_f = self.model.predict(np.array([state]))

            #print("Q targets old: ", target_f)

            target_f[0][action] = target

            #print("Q targets new: ", target_f)

            #print("target check: ", target_f[0][action])
            #target_f[0][np.argmax(action)] = target
            #self.model.fit (np.array([state]), target_f, epochs=1, verbose = 1, callbacks=[self.history])
            self.model.fit (np.array([state]), target_f, epochs=1, verbose = 0)
            #print("Q prediction: ", self.model.predict(np.array([state]))[0])
            

    def train_short_memory(self,state,action,reward,next_state,done) : #training online after each decision straightaway? vs the long-term batch sampling
        target = reward #target is the estimation of the correct q-value
            # sets the target equal to reward or estimation of what that is if game isn't finished
        if not done:
            target = reward + self.gamma * np.amax(self.model.predict(next_state.reshape((1,(self.dim**2+8))))[0])
        target_f = self.model.predict(np.array([state])) 
        #target_f[0][np.argmax(action)] = target



        target_f[0][action] = target
        self.model.fit (state.reshape((1,(self.dim**2+8))), target_f, epochs=1, verbose = 0)
