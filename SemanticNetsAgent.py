
   

import queue

class SemanticNetsAgent:
    def __init__(self, variables=(1, 1, 1), no_of_moves=0, move=(0, 0), parent_state=None):   
        #State variables
        self.vars = variables
        #Number of moves taken to reach the current state
        self.no_of_moves = no_of_moves
        #To keep track of the path from the initial state to the current state.
        self.parent_state = parent_state
        self.move = move
    #Check All valid conditions
    def authenticate(self, initial_Sheeps, initial_Wolves):

        sheep, wolves, boat = self.vars
          #No of sheeps must be greater then 0 or initial_sheeps
        if sheep < 0 or sheep > initial_Sheeps:
            return False
           #No of wolves must be greater then 0 or initial_sheeps
        elif wolves < 0 or wolves > initial_Wolves:
            return False
        return True
    #Check if the current state is solution or not
    def check_solution(self):
        if self.vars == (0, 0, 0):
            return True
        return False
    
    def next_states(self, initial_Sheep, initial_Wolves):
        moves = [(1, 1), (1, 0), (0, 1), (2, 0), (0, 2)]
        all_states = []
        right_sheeps, right_wolves, right_boat = self.vars
        #Add and remove the move based on the boat 
        #If the boat on right remove the move or if the boat on left add the move  
        for move in moves:
            update_sheeps, update_wolves = move
            if right_boat == 1:
                 #Decrement because we move on right side
                 #0 is indicating left because after going to right we have to move left
                new_vars = (right_sheeps - update_sheeps, right_wolves - update_wolves, 0)
            else:
                 #Increment because we move on left side
                 #1 is indicating right because after going to left we have to move right
                new_vars = (right_sheeps + update_sheeps, right_wolves + update_wolves, 1)
             # Increase the no. of moves by 1
            new_state = SemanticNetsAgent(new_vars, self.no_of_moves + 1, move, self)
            if new_state.authenticate(initial_Sheep, initial_Wolves):
                all_states.append(new_state)

        return all_states, move
    
    #Check if the current state is failure or not
    def check_failure(self, initial_Sheeps, initial_Wolves):
        sheep, wolves, boat = self.vars

        if sheep > 0 and sheep < wolves:
            return True
         #Get the remaining sheeps on left side
        left_sheeps = initial_Sheeps - sheep
         #Get the remaining wolf on left side
        left_wolves = initial_Wolves - wolves

        if left_sheeps > 0 and left_sheeps < left_wolves:
            return True
        return False

    

    def sheep_wolf_sol(self, initial_Sheeps, initial_Wolves):
        startState = self.__class__((initial_Sheeps, initial_Wolves, 1))
        #To keep the track of the states
        #We will append the possible state to visit in future_states
        future_states = queue.Queue()
        #For storing all the visited states
        visited = set()
        #For storing the posible states
        solutions = []

        future_states.put(startState)
        #Run until queue is empty
        while not future_states.empty():
            #Get the next state from queue
            current_state = future_states.get()
            #Checking if current state is solution or not
            if current_state.check_solution():
             # If the current state is a solution state, backtrack to get the moves
                results = []
                while current_state.parent_state:
                    results.append(current_state.move)
                    current_state = current_state.parent_state
                results.reverse()
                return results
            #If current state is not in visited and does not voilate condition
            #then append in visited
            if current_state.vars not in visited and not current_state.check_failure(initial_Sheeps, initial_Wolves):
                # Mark the current state as visited
                visited.add(current_state.vars)
                next_states, _ = current_state.next_states(initial_Sheeps, initial_Wolves)
                # Add the next states to the queue
                future_states.queue.extend(next_states)
        # No solution found, return an empty list
        return []
