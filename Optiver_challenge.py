'''Can you write a program that comes up with an estimate of average time to find food for any closed boundary around the anthill? 
What would be the answer if food is located outside an defined by ( (x – 2.5cm) / 30cm )2 + ( (y – 2.5cm) / 40cm )2 < 1 in 
coordinate system where the anthill is located at (x = 0cm, y = 0cm)? Provide us with a solution rounded to the nearest integer.'''

import numpy as np
from progressbar import ProgressBar

class random_walk_ant:
    def __init__(self, ant_number=100000, x_start=0.0, y_start=0.0, delta=1, speed=10):
        self.ant_number = ant_number                           # Number of ants we release
        self.start_x, self.start_y = x_start, y_start          # starting x and y coordinate
        self.xy_positions = self.make_position_array()   # initialized array of particle positions
        self.time = self.make_time_array()               # initialized array of particle time
        self.delta = delta                                           # integration timestep (seconds)
        self.speed = speed                                         # walk speek (cm / s)
        
    def make_position_array(self):
        # Initializing the array in which we store the ants' x and y positions -> n_samples*2
        xy_positions = np.zeros(shape=(self.ant_number, 2))
        xy_positions[:, 0] = self.start_x #set starting x coordinate
        xy_positions[:, 1] = self.start_y #set starting y coordinate
        
        return xy_positions
    
    def make_time_array(self):
        return np.zeros(shape=(self.ant_number))
        
    def random_walk(self, xy_positions):
        # Generate an array with random integers between 0 - 3 which will set the direction of the random walks
        walk_direction = np.random.randint(low=0, high=4, size=self.ant_number)
        
        # If walk_direction == 0, move north by v0 * dt
        north = np.where(walk_direction == 0)[0]
        xy_positions[north, 1] += self.delta * self.speed
        # if walk_direction == 1, move south by v0 * dt
        south = np.where(walk_direction == 1)[0]
        xy_positions[south, 1] -= self.delta * self.speed
        # if walk_direction == 2, move east by v0 * dt
        east = np.where(walk_direction == 2)[0]
        xy_positions[east, 0] += self.delta * self.speed
        # if walk_direction == 3, move west by v0 * dt
        west = np.where(walk_direction == 3)[0]
        xy_positions[west, 0] -= self.delta * self.speed
        
        return xy_positions
    
    def calculate_walk(self, steps):
        for i in ProgressBar()(range(steps)):
            # Calculate the random walk procedure
            self.xy_positions = self.random_walk(self.xy_positions)
            # Update the time tracker of each ant that has not crossed boundary yet
            self.time[~np.isnan(self.xy_positions[:, 0])] += 1
            # Set to np.nan all particles that are at or have crossed the boundary condition
            at_boundary = self.boundary_condition()
            self.xy_positions[at_boundary, :] = np.nan
            
        return self.xy_positions, self.time

    def boundary_condition(self):
        boundary = np.square((self.xy_positions[:, 0] - 2.5) / 30) + np.square((self.xy_positions[:, 1] - 2.5) / 40) >= 1
        return boundary
    
    def calculate_mean_travel_time(self, steps=1000):
        self.xy_positions, self.time = self.calculate_walk(steps=steps)
        # Determine the particles that are at the food
        at_food = np.isnan(self.xy_positions[:, 0])
        # Calculate the mean time
        mean_time = self.time[at_food].mean()
        std_time = self.time[at_food].std()
        error_time = std_time / np.sqrt(np.sum(at_food))
        
        # Calculate the number of ants that have reached the food
        at_food_percentage = np.sum(at_food) / self.ant_number * 100
        
        str_format = mean_time, error_time
        print('It takes an ant {:.2f}±{:.2f} seconds on an average to encounter food.'.format(*str_format))



obj = random_walk_ant(ant_number = 100000)
obj.calculate_mean_travel_time()

  
  

