import mesa
import random
import math
import time
# import pdb
# pdb.set_trace()  # set a breakpoint



class InfoAgent(mesa.Agent):

    def __init__(self, pos, model, personality, message, condition="Unaware"):
        """ Create a new agent. """

        super().__init__(pos, model)
        self.pos = pos
        self.action_queue = [self.wait]
        self.personality_type = personality[0]
        self.parameters = personality[1]
        self.condition = condition

        self.sensitivity_index = 1#personality["neuroticism"]
        self.contagion_parameter = 0.1
        self.social_reinforcement_factor = 0.1
        self.amount_of_tries = 0
        self.wait_counter = 0

        urgency, complexity = message.split(" - ")
        self.message = Message('Go to Exit', urgency, complexity)


    def step(self):
        """
        Things the agent should try to do in this order:

        1. If the agent is informed, spread it to uninformed agents nearby.
            -> based on the "spread_chance" probability 
        2. If the agent is listening, the information is analyzed with two outcomes:
            -> agents turns "Informed"/"Unaware" based on "receive_chance" probability
                -> and "Misinformed" based on "misinfo_chance" probability
        """
        # Get the next action from the action_queue
        next_action = self.action_queue[0]

        #Execute the next action
        next_action()


    # Condition: "Disseminative" -> "Informed" (done)
    def share_information(self):

        # Select neighbor based on dij
        neighbor = self.choose_neighbor()

        if neighbor:
  
            # Try to pass on the message
            if random.random() < neighbor.sensitivity_index:
                neighbor.action_queue = [neighbor.accept_information]
                neighbor.message = self.message
            
            self.condition = "Informed"
            self.action_queue= [self.try_disseminate]
            #TODO: Mark sender as +1 or smth -> can only send once  
        else:            
            self.condition = "Informed"
            self.action_queue = [self.wait]



    # Condition: "Unaware" -> "Informed"
    def accept_information(self):
        # TODO: b -> social reinforcement || m -> amount of tries || x -> openess/ extraversion
        b = 0.8#self.social_reinforcement_factor
        m = 2#self.amount_of_tries
        x = 0.3#self.contagion_parameter

        accept_chance = 1 - (1 - x) * math.exp(-b * (m - 1))
        # print(f"accept_chance {accept_chance}")


        if random.random() < accept_chance:
            self.condition = "Informed"
            self.action_queue = [self.try_disseminate]
        else:
            self.condition = "Unaware"
            self.action_queue = [self.wait]


    # Condition: "Informed" -> "Disseminative" / "Panic" -> "Exhausted"
    def try_disseminate(self):
        #TODO: panic, disseminate y -> neuroticism
        choose_dissemination = 0.8 # 1- self.neuroticism
        choose_panic = 0.1 #self.neuroticism

        if random.random() < choose_dissemination:
            self.condition = "Disseminative"
            self.action_queue = [self.share_information]

        elif random.random() < choose_panic:
            self.condition = "Panic"
            self.action_queue = [self.wait]


    def choose_neighbor(self):
        #TODO: give agents 'priority_factor' -> choose neighbor with highest priority

        # Find nearby agents
        neighbors = (n for n in self.model.grid.get_neighbors(self.pos, moore=True, include_center=False) if n.condition == "Unaware")
        
        priority_factor = 0
        

        try:
            target = next(neighbors)
        except StopIteration:
            print("No neighbor found.")
            target = ""
        return target



    def wait(self):
        if self.condition == "Panic":
            if self.wait_counter < 10:
                self.wait_counter += 1
            else:
                self.condition = "Exhausted"
                self.wait_counter = 0
        else:
            # Handle the case when the condition is not "Panic"
            pass

    
    def __str__(self):
            action_queue_str = [f"{func.__name__}" for func in self.action_queue] # this line has changed
            return f"Agent {self.unique_id}: condition={self.condition}, action_queue={action_queue_str}"


class Message:
    def __init__(self, topic, urgency, complexity, misinfo = False):
        self.topic = topic
        self.urgency = urgency
        self.complexity = complexity
        self.misinfo = misinfo


    def __str__(self):
        return f"Message: topic={self.topic}, urgency={self.urgency}, complexity={self.complexity}, misinfo={self.misinfo}"


