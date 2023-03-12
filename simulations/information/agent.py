import mesa


class InfoAgent(mesa.Agent):

    def __init__(self, pos, model, spread_chance, receive_chance, misinfo_chance, condition="NoInfo", misinformed= False):
        """ Create a new agent. """

        super().__init__(pos, model)
        self.pos = pos
        self.condition = condition
        self.spread_chance = spread_chance
        self.receive_chance = receive_chance
        self.misinfo_chance = misinfo_chance
        self.misinformed = misinformed
        

    def step(self):
        """
        Things the agent should try to do in this order:

        1. If the agent is informed, spread it to uninformed agents nearby.
            -> based on the "spread_chance" probability & "misinfo_chance" probability

        2. If the agent is listening, the information is analyzed with two outcomes:
            -> agents turns "Informed"/"NoInfo" based on "receive_chance" probability
        """

        if self.condition == "Informed" or self.condition == "Misinformed":
            self.try_to_inform_neighbors()
          
        elif self.condition == "Listening":
            if self.random.random() < self.receive_chance:
                if self.misinformed or (self.random.random() < self.misinfo_chance):
                    self.condition = "Misinformed"
                    self.misinformed = True
                else: 
                    self.condition = "Informed"
            else:
                self.condition = "NoInfo"
 

    def try_to_inform_neighbors(self):
        for neighbor in self.model.grid.iter_neighbors(self.pos, True):
            if neighbor.condition == "NoInfo":
                if self.random.random() < self.spread_chance:
                    if self.misinformed: # if the agent is already misinformed
                        neighbor.condition = "Listening"
                        neighbor.misinformed = True
                    else:
                        neighbor.condition = "Listening"
 
              
    
    
    
        # for neighbor in self.model.grid.iter_neighbors(self.pos, True):
        #     if neighbor.condition == "NoInfo":
        #         if self.random.random() < self.spread_chance:
        #             neighbor.condition = "Listening"

        # for a in susceptible_neighbors:
        #     if self.random.random() < self.spread_chance:
        #         a.condition = "Listening"


 
    # def step(self):
    #     """
    #     If the person is listening, spread it to uninformed people nearby.
    #     """
    #     if self.condition == "Listening":
    #         for neighbor in self.model.grid.iter_neighbors(self.pos, True):
    #             if neighbor.condition == "NoInfo":
    #                 neighbor.condition = "Listening"
    #         self.condition = "Informed"


    # def try_to_infect_neighbors(self):
    #     neighbors_nodes = self.model.grid.get_neighbors(self.pos, include_center=False)
    #     susceptible_neighbors = [
    #         agent
    #         for agent in self.model.grid.get_cell_list_contents(neighbors_nodes)
    #         if agent.condition == "NoInfo"
    #     ]
    #     for a in susceptible_neighbors:
    #         if self.random.random() < self.spread_chance:
    #             a.condition = "Listening"

    

    # def step(self):
    #     if self.condition == "Informed":
    #         self.try_to_infect_neighbors()
    #     self.try_check_situation()