import mesa
import random
import math
import time
# import pdb
# pdb.set_trace() # set a breakpoint



class InfoAgent(mesa.Agent):

    def __init__(self, pos, model, personality, density, condition="Unaware"):
        """ Create a new agent. """

        super().__init__(pos, model)
        self.pos = pos
        self.action_queue = [self.wait]
        self.personality_name = personality[0]
        self.personality_values = personality[1]
        self.condition = condition
        self.is_disseminative = False
        self.density = density

        self.amount_of_tries = 1
        self.wait_counter = 0

        # urgency, complexity = message.split(" - ")
        self.message = Message('Go to Exit', "urgency", "complexity")


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
        if not self.personality_name == 'heterogeneous':

            # Select neighbor based on dij
            neighbor = self.choose_neighbor()

            if neighbor:
    
                neighbor.action_queue = [neighbor.accept_information]
                neighbor.message = self.message
            
                self.condition = "Informed"
                self.action_queue= [self.try_disseminate]
            
            else:            
                self.condition = "Informed"
                self.action_queue = [self.wait]
        else:
            pass



    # Condition: "Unaware" -> "Informed"
    def accept_information(self):
        if not self.personality_name == 'heterogeneous':
            b = 0.2 # social_reinforcement_factor
            m = self.amount_of_tries
            x = self.personality_values['agreeableness']

            accept_chance = 1 - (1 - x) * math.exp(-b * (m - 1))
            # print(f"accept_chance {accept_chance} from agent {self}")


            if random.random() < accept_chance:
                self.condition = "Informed"
                self.action_queue = [self.try_disseminate]
            else:
                self.condition = "Unaware"
                self.amount_of_tries += 1
                self.action_queue = [self.wait]
        else:
            pass


    # Condition: "Informed" -> "Disseminative" / "Stressed" -> "Exhausted"
    def try_disseminate(self):
        if not self.personality_name == 'heterogeneous':
            
            neuroticism = (self.personality_values['neuroticism']/4) * self.density
            
            # choose_dissemination = self.personality_values['extraversion']
            # decision_index = (1- self.personality_values['neuroticism'])

            u = random.random()
            # print(f"u {u}, extra {1-neuroticism}, Stressed {neuroticism}, agent {self.pos}")
            
            if u >= neuroticism: 
                self.condition = "Disseminative"
                self.action_queue = [self.share_information]
                self.is_disseminative = True


            elif u < neuroticism: 
                if not self.is_disseminative and not self.pos == (0,0):
                    self.condition = "Stressed"
                    self.action_queue = [self.wait]
            
                # else:
                #     print(f"This agent this nothing: {self}")

        else:
            pass


    def choose_neighbor(self):
        # Find nearby agents and calculate priority index in a single pass
        max_priority_index = 0
        max_priority_neighbors = []

        for neighbor in self.model.grid.get_neighbors(self.pos, moore=True, include_center=False):
            if neighbor.condition == "Unaware":
                unaware_count = sum(1 for n in self.model.grid.get_neighbors(neighbor.pos, moore=True) if n.condition == "Unaware")

                if unaware_count > max_priority_index:
                    max_priority_index = unaware_count
                    max_priority_neighbors = [neighbor]
                elif unaware_count == max_priority_index:
                    max_priority_neighbors.append(neighbor)

        if not max_priority_neighbors:
            # print("No neighbor found.")
            return None

        # Randomly select one of the neighbors with the highest priority index
        target = random.choice(max_priority_neighbors)
        return target



    def wait(self):
        if self.condition == "Stressed":
            if self.wait_counter < 10:
                self.wait_counter += 1
            else:
                self.condition = "Exhausted"
                self.wait_counter = 0
        else:
            # Handle the case when the condition is not "Stressed"
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


