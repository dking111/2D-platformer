import sqlite3
import numpy as np
import random

from constants import KD_RANGE,VEL_RANGE, DISPLAY_WIDTH,TILE_SIZE

class Q_table:
    """Is able to create and manipulate the Q_table"""
    def __init__(self):
        self.table_length = self.get_length()
        self.table = []

    def set_table(self):
        #Creates a partially completed Q-table
        with sqlite3.connect("./DB/game.db") as db:                                         #connects DB
            cursor = db.cursor()
            cursor.execute('DELETE FROM Q_table;',);                                        #deletes existing data
            
            for i in range(0,KD_RANGE*VEL_RANGE):
                m = ((i%VEL_RANGE)+1)*(i/KD_RANGE)/10                                       #multiplier VEL
                values = (i,0.5*m,0,-0.5*m,0.5*m,0,-0.5*m,0.5*m,0,-0.5*m,0.5*m,0,-0.5*m)    #inserted values
                cursor.execute("INSERT INTO Q_table(STATE,ACTION_1,ACTION_2,ACTION_3,ACTION_4,ACTION_5,ACTION_6,ACTION_7,ACTION_8,ACTION_9,ACTION_10,ACTION_11,ACTION_12) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)",values)
                db.commit()

    def get_length(self):
        #gets length of Q-table
        with sqlite3.connect("./DB/game.db") as db:                      #connects DB
            cursor = db.cursor()
            cursor.execute("SELECT COUNT(*) FROM Q_table")                  #SQL          
            return cursor.fetchone()[0]
    
    def set_value(self,state,column,value):
        #sets a specific value within the Q-table
        with sqlite3.connect("./DB/game.db") as db:                                                      #connects DB
            cursor = db.cursor()                                                                        
            cursor.execute("UPDATE Q_table SET ACTION_"+str(column)+" = ? WHERE STATE = ?",(value,state))   #SQL
            db.commit()
    
    def get_entry(self,state):
        #gets one entry from the Q-table                                                         
        with sqlite3.connect("./DB/game.db") as db:                      #connects DB
            cursor = db.cursor()
            cursor.execute("SELECT * FROM Q_table where STATE =?",(state,)) #SQL
            entry = cursor.fetchone()
            return entry                                                    #returns array

class Learn:
    """Controls learning process and interactions with Q-table"""
    def __init__(self,perlin_dif,projectile_dif,melee_dif,platform_dif):
        self.Q_table = Q_table()                #creates instant of Q-table class
        Q_table().set_table()                   #resets table
        #RL equation
        self.epsilon = 0.9                      #controls the learning rate of the algorithm
        self.alpha = 0.1
        self.gamma = 0.6
        #given values
        self.perlin_dif = perlin_dif            #difficulty values - will be returned to generator
        self.projectile_dif = projectile_dif
        self.melee_dif = melee_dif
        self.platform_dif = platform_dif
        #state
        self.set_state_space()                  #creates state space
        self.state = 0
        #
        self.time_taken = 0                     #time taken for 1 batch to pass
        

    def learn(self,passthrough,time_taken,kills_for_batch,deaths_for_batch):
        #called each time a batch is complete, calls every other method
        #updating epsilon
        if self.epsilon != 0:
            self.epsilon -= 0.01
        #batch calcuations
        try:
            batch_VEL = (DISPLAY_WIDTH/TILE_SIZE)/time_taken    #VEL = distance/time
        except ZeroDivisionError:
            batch_VEL = 0
        try: 
            batch_KD = kills_for_batch/deaths_for_batch         #KD = kills/death
        except ZeroDivisionError:
            batch_KD = 1

        KD = passthrough[0]                                     #gets KD from generator passthrough
        VEL = passthrough[1]                                    #gets VEL from generator passthrough
        #calls other methods
        self.calc_action(KD,batch_VEL)                          #finds correct action
        self.do_action(self.action)                             #does correct action
        self.update_table(KD,VEL,batch_KD,batch_VEL)            #evaluates action
        #back to generator
        return self.melee_dif, self.projectile_dif,self.perlin_dif,self.platform_dif

    def set_state_space(self):
        #called at start, creates state space
        self.state_space = np.zeros((KD_RANGE,VEL_RANGE))       #creates array of zeros
        for i in range(0,len(self.state_space)):
            for j in range(0,len(self.state_space[i])):
                self.state_space[i][j] = i*VEL_RANGE + j        #adds ordered numbers to array
        

    def get_state(self,KD,VEL):
        #finds state from given data
        if KD >= KD_RANGE:                                       #sets boundary for KD
            KD = KD_RANGE - 1
        if VEL >= VEL_RANGE:                                     #sets boundary for VEL
            VEL = VEL_RANGE - 1
        self.state = self.state_space[int(KD),(int(VEL))]       #input into array
        return self.state                                       #back to self.calc_action()


    def calc_action(self,KD,VEL):
        #calculates the corerct action to take
        self.state = self.get_state(KD,VEL)                     #gets state
        entry = self.Q_table.get_entry(self.state)              #get entry at that state

        if random.uniform(0,1) < self.epsilon:                  #compares epsilon value
            action = random.randint(1,12)                       #takes random action
        else:
            max = 0
            maxi = 1
            for i in range(len(entry)):                         #finds max Q value in state
                if entry[i] > max:
                    max = entry[i] 
                    maxi = i
            action = maxi +1
        self.action = action                                    #action taken is the one withe the highest Q value

    def do_action(self,action):
        #executes the appropriate action
        match action:                                           #uses a switch statement 
            case 1:
                self.melee_dif += 0.1
            case 3:
                self.melee_dif -= 0.1
            case 4: 
                self.projectile_dif += 0.1
            case 6:
                self.projectile_dif -= 0.1
            case 7:
                self.platform_dif += 0.1
            case 9: 
                self.platform_dif -= 0.1
            case 10:
                self.perlin_dif += 0.1
            case 12:
                self.perlin_dif -= 0.1
            case _ : 
                pass
        #boundaries
        if self.melee_dif > 1:                                  #sets boundaries for melee dif
            self.melee_dif = 1
        elif self.melee_dif < 0:
            self.melee_dif = 0

        if self.projectile_dif > 1:                             #sets boundaries for projectile dif
            self.projectile_dif = 1
        elif self.projectile_dif < 0:
            self.projectile_dif = 0

        if self.perlin_dif > 1:                                 #set boundaries for perlin dif
            self.perlin_dif = 1
        elif self.perlin_dif < 0:
            self.perlin_dif = 0

        if self.platform_dif > 1:                               #sets boundaries for platform dif
            self.platform_dif = 1
        elif self.platform_dif < 0:
            self.platform_dif = 0

    def update_table(self,KD,VEL,batch_KD,batch_VEL):
        #evaluates last action then changes Q-table
        reward = 0
        if batch_VEL >= VEL:                                                                    #compares batches velocity to average velocity
            reward -= 2                                                     
            if batch_VEL > VEL+1:
                reward -=2
        elif batch_VEL < VEL:
            reward += 3
            if batch_VEL < VEL - 1:
                reward += 2
        
        if batch_KD >= KD:                                                                      #compares batches KD to average KD
            reward -= 2
            if batch_KD > KD+1:
                reward -=2
        elif batch_KD < KD:
            reward += 3
            if batch_KD < KD - 1:
                reward += 2
        
        old_value = self.Q_table.get_entry(self.state)[self.action]                             #finds old Q-value of state
        Q_value = (1-self.alpha) * float(old_value) + self.alpha * (reward + self.gamma)        #calcualtes new Q_value
        self.Q_table.set_value(self.state,self.action,Q_value)                                  #commits new Q-value to table



