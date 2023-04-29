import mesa
import random
import time
# import pdb
# pdb.set_trace()  # set a breakpoint



class InfoAgent(mesa.Agent):

    def __init__(self, pos, model, personality, message, misinfo_chance, condition="NoInfo" , misinformed= False):
        """ Create a new agent. """

        super().__init__(pos, model)
        self.pos = pos
        self.action_queue = [self.wait]
        self.parameters = personality
        self.motives = ['physical', 'emotional', 'social']
        self.friends = []
        self.misinfo_chance = misinfo_chance
        self.condition = condition
        self.misinformed = misinformed
        urgency, complexity = message.split(" - ")
        self.message = Message('Go to Exit', urgency, complexity)


    def step(self):
        """
        Things the agent should try to do in this order:

        1. If the agent is informed, spread it to uninformed agents nearby.
            -> based on the "spread_chance" probability 
        2. If the agent is listening, the information is analyzed with two outcomes:
            -> agents turns "Informed"/"NoInfo" based on "receive_chance" probability
                -> and "Misinformed" based on "misinfo_chance" probability
        """
        # Get the next action from the action_queue
        next_action = self.action_queue[0]

        #Execute the next action
        next_action()



    def share_information(self):
        spread_chance = self.calculate_spread_chance(self.message)

        # Find nearby agents
        neighbors = (n for n in self.model.grid.get_neighbors(self.pos, moore=True, include_center=False) if n.condition == "NoInfo")

        for neighbor in neighbors:
            
            # Try to pass on the message to nearby agents
            if random.random() < spread_chance:
                neighbor.condition = "Listening"
                neighbor.action_queue = [neighbor.receive_information]
                neighbor.message = self.message
               
                if self.misinformed: # if the agent is already misinformed
                    neighbor.misinformed = True


    def receive_information(self):
        receive_chance = self.calculate_receive_chance(self.message)

        if random.random() < receive_chance:
            if self.misinformed:
                self.condition = "Misinformed"
                self.action_queue = [self.share_information]
            else: 
                self.condition = "Informed"
                self.action_queue = [self.share_information]

        else:
            self.condition = "NoInfo"
            self.action_queue = [self.wait]



    def wait(self):
        # Do nothing (action_queue default).
        pass


    def calculate_spread_chance(self, message):
        """
        Tries to find the average between the agents: sociality, perceived_risk and confidence 
            message.urgency should influence perceived_risk

        """
        sociality, perceived_risk, confidence = self.parameters['sociality'], self.parameters['perceived_risk'], self.parameters['confidence']

        # If the message is complex, increase risk perceivement
        if message.urgency == 'high':
            perceived_risk *= 1.8

        # Calculate the average spread chance
        spread_chance = (sociality + perceived_risk + confidence) / 3
        return spread_chance


    def calculate_receive_chance(self, message):
        """
        Tries to find the average between the agents: sociality, knowledge and trust
            message.complexity should influence knowledge

        """
        sociality, knowledge, trust = self.parameters['sociality'], self.parameters['knowledge'], self.parameters['trust']

        # If the message is complex, lower knowledge
        if message.complexity == 'high':
            knowledge *= 0.8

        # If the message is too complex, the agents misunderstands.
        if self.misinfo_chance > knowledge:
            self.misinformed = True

        # Calculate the average spread chance
        receive_chance = (sociality + knowledge + trust) / 3
        return receive_chance
    
    
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
