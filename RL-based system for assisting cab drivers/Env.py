# Import routines

import numpy as np
import math
import random

# Defining hyperparameters
m = 5 # number of cities, ranges from 1 ..... m
t = 24 # number of hours, ranges from 0 .... t-1
d = 7  # number of days, ranges from 0 ... d-1
C = 5 # Per hour fuel and other costs
R = 9 # per hour revenue from a passenger


class CabDriver():

    def __init__(self):
        """initialise your state and define your action space and state space"""
        self.action_space = [[i,j] for i in range(5) for j in range(5) if (i!=j) or ((i==0) and (j==0))] 
        self.state_space = [[i,j,k] for i in range(5) for j in range(24) for k in range(7)]
        self.state_init = random.choice(self.state_space)

        # Start the first round
        self.reset()


    ## Encoding state (or state-action) for NN input

    def state_encod_arch1(self, state):
        """convert the state into a vector so that it can be fed to the NN. This method converts a given state into a vector format. Hint: The vector is of size m + t + d."""
        state_encod = np.zeros(m+t+d)
        state_index=state[0]
        time_index = m + state[1]
        day_index = m + t + state[2]
        #print(state_index,time_index,day_index)
        state_encod[state_index] = 1
        state_encod[time_index] = 1
        state_encod[day_index] = 1
        return state_encod


    # Use this function if you are using architecture-2 
    def state_encod_arch2(self, state, action):
         """convert the (state-action) into a vector so that it can be fed to the NN. This method converts a given state-action pair into a vector format. Hint: The vector is of size m + t + d + m + m."""
        #state_encod = np.zeros(m+t+d+m+m)
        #state_encod[state[0]] = 1
        #state_encod[m+state[1]] = 1
        #state_encod[m+t+state[2]] = 1
        #state_encod[m+t+d+action[0]] = 1
        #state_encod[m+t+d+m+action[1]] = 1 
        #return state_encod

        
    #     return state_encod


    ## Getting number of requests

    def requests(self, state):
        """Determining the number of requests basis the location. 
        Use the table specified in the MDP and complete for rest of the locations"""
        location = state[0]
        if location == 0:
            requests = np.random.poisson(2)
        elif location == 1:
            requests = np.random.poisson(12)
        elif location == 2:
            requests = np.random.poisson(4)
        elif location == 3:
            requests = np.random.poisson(7)
        elif location == 4:
            requests = np.random.poisson(8)
        if requests >15:
            requests =15

        possible_actions_index = random.sample(range(1, (m-1)*m ), requests) # (0,0) is not considered as customer request
        actions = [self.action_space[i] for i in possible_actions_index]

        
        actions.append([0,0])

        return possible_actions_index,actions   

    def new_time(self,time,day,time_taken):
        new_time_of_day = time + math.ceil(time_taken)
        new_day_of_week = day
        if new_time_of_day > 23:
            new_time_of_day = new_time_of_day % 24
            new_day_of_week += 1
            if new_day_of_week > 6:
                new_day_of_week = new_day_of_week % 7
        #print("New_time ",new_time_of_day,new_day_of_week)
        return new_time_of_day,new_day_of_week

    def reward_func(self, state, action, Time_matrix):
        """Takes in state, action and Time-matrix and returns the reward"""
        reward = 0
        cab_pos = state[0]
        pickup_pos = action[0]
        drop_pos = action[1]
        time_of_day = state[1]
        day_of_week = state[2]
        new_time_of_day = time_of_day #variable to calculate the time when cab reached pickup posiion if curr_pos != pickup_pos
        new_day_of_week = day_of_week #variable to calculate the day of week when cab reached pickup posiion if curr_pos != pickup_pos
        
        if cab_pos!=pickup_pos: #Calculate the new time of day and week when cab reaches pickup position
            time_taken = Time_matrix[cab_pos][pickup_pos][time_of_day][day_of_week]
            new_time_of_day,new_day_of_week = self.new_time(time_of_day,day_of_week,time_taken) 
        
        if (pickup_pos == 0) and (drop_pos==0):
            reward = -C
        else:
            #print(pickup_pos,drop_pos,new_time_of_day,new_day_of_week)
            reward = R*Time_matrix[pickup_pos][drop_pos][new_time_of_day][new_day_of_week] - C*(Time_matrix[pickup_pos][drop_pos][new_time_of_day][new_day_of_week] + Time_matrix[cab_pos][pickup_pos][time_of_day][day_of_week])
        
        return reward


    def next_state_func(self, state, action, Time_matrix):
        """Takes state and action as input and returns next state"""
        next_state = []
        cab_pos = state[0]
        pickup_pos = action[0]
        drop_pos = action[1]
        time_of_day = state[1]
        day_of_week = state[2]
        new_time_of_day = time_of_day #variable to calculate the time when cab reached pickup posiion if curr_pos != pickup_pos
        new_day_of_week = day_of_week #variable to calculate the day of week when cab reached pickup posiion if curr_pos != pickup_pos
        total_time = 0
        if cab_pos!=pickup_pos: #Calculate the new time of day and week when cab reaches pickup position
            time_taken = Time_matrix[cab_pos][pickup_pos][time_of_day][day_of_week]
            new_time_of_day,new_day_of_week = self.new_time(time_of_day,day_of_week,time_taken)
            total_time += time_taken
        
        if (pickup_pos == 0) and (drop_pos==0):
            total_time += 1
            new_time_of_day,new_day_of_week = self.new_time(time_of_day,day_of_week,1)
            next_state = [cab_pos,new_time_of_day,new_day_of_week]
        else:
            time_taken = Time_matrix[pickup_pos][drop_pos][new_time_of_day][new_day_of_week]
            total_time += time_taken
            final_time_of_day,final_day_of_week = self.new_time(new_time_of_day,new_day_of_week,time_taken)
            next_state = [drop_pos,final_time_of_day,final_day_of_week]
        return next_state,total_time




    def reset(self):
        return self.action_space, self.state_space, self.state_init