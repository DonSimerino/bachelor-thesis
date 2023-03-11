import mesa
from agent import InfoAgent


class InfoModel(mesa.Model):
    """A agent model with some number of agents"""
    
    height = 25 
    width = 25

    @classmethod
    def update_values(cls, new_height, new_width):
        print("im inside update")
        print("cls hi " + str(cls.height))
        cls.height = new_height
        cls.width = new_width

    def __init__(
            self,
            width=20, 
            height=20, 
            num_nodes=10, 
            density=0.65,
            initial_outbreak= 1,
            spread_chance= 1,
            receive_chance= 1,
            misinfo_chance=0.4,
            police_chance=0.0):
        

        self.num_nodes = num_nodes
        self.density = density
        self.initial_outbreak = (
            initial_outbreak if initial_outbreak <= num_nodes else num_nodes
        )
        self.spread_chance = spread_chance
        self.receive_chance = receive_chance
        self.misinfo_chance = misinfo_chance
        self.police_chance = police_chance

        
        self.schedule = mesa.time.RandomActivation(self)
        
        # Grid Size (agents) is equal and adjusts accordingly to the number of agents 
        self.grid = mesa.space.Grid(self.height, self.width, torus=False)
     
        self.datacollector = mesa.datacollection.DataCollector(
            {
                "NoInfo": lambda m: self.count_type(m, "NoInfo"),
                "Listening": lambda m: self.count_type(m, "Listening"),
                "Informed": lambda m: self.count_type(m, "Informed"),
                "Misinformed": lambda m: self.count_type(m, "Misinformed"),
            }
        )

        # Create Agents
        agent_tuple_list = []
        for (contents, x, y) in self.grid.coord_iter():
            if self.random.random() < density:

                agent = InfoAgent((x, y), self, self.spread_chance, self.receive_chance, self.misinfo_chance)

                # Set agents in the bottom left corner to listening.
                if x == 0 and y == 0:
                    agent.condition = "Informed"
                
                self.grid.place_agent(agent, (x, y))
                self.schedule.add(agent)
                agent_tuple_list.append((x, y))

 
        # Randomly infect some nodes based on "initial_outbreak"
        infected_nodes = self.random.sample(agent_tuple_list, self.initial_outbreak-1)
        for a in self.grid.get_cell_list_contents(infected_nodes):
            a.condition = "Informed"

        self.running = True
        self.datacollector.collect(self)

    def step(self):
        self.schedule.step()
        # collect data
        self.datacollector.collect(self)
        # Halt if no more info
        if self.count_type(self, "NoInfo") == 0 and self.count_type(self, "Listening") == 0:
            self.running = False


    @staticmethod
    def count_type(model, person_condition):
        """
        Helper method to count agents in a given condition in a given model.
        """
        count = 0
        for agent in model.schedule.agents:
            if agent.condition == person_condition:
                count += 1
        return count
