import mesa

# from model import InfoModel

class InfoAgent(mesa.Agent):
    """

    Attributes:
        x, y: Grid coordinates
        condition: Can be "NoInfo", "Listening", or "Informed"
        unique_id: (x,y) tuple.

    unique_id isn't strictly necessary here, but it's good
    practice to give one to each agent anyway.
    """

    def __init__(self, pos, model, spread_chance):
        """
        Create a new agent.
        """
        super().__init__(pos, model)
        self.pos = pos
        self.condition = "NoInfo"
        self.spread_chance = spread_chance

  
    def step(self):
        """
        If the person is listening, spread it to uninformed people nearby.
        """
        if self.condition == "Listening":
            for neighbor in self.model.grid.iter_neighbors(self.pos, True):
                if neighbor.condition == "NoInfo":
                    neighbor.condition = "Listening"
            self.condition = "Informed"



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
            spread_chance= 0.4,
            misinfo_chance=0.0,
            police_chance=0.0):
        
        # self.width = 7
        # self.height = 7
        # self.update_values(10, 10)


        self.num_nodes = num_nodes
        self.density = density
        self.initial_outbreak = (
            initial_outbreak if initial_outbreak <= num_nodes else num_nodes
        )
        self.spread_chance = spread_chance
        self.misinfo_chance = misinfo_chance
        self.police_chance = police_chance

        
        self.schedule = mesa.time.RandomActivation(self)
        
        # Grid Size (agents) is equal and adjusts accordingly to the number of agents 
        self.grid = mesa.space.Grid(25, 25, torus=False)

        self.datacollector = mesa.datacollection.DataCollector(
            {
                "NoInfo": lambda m: self.count_type(m, "NoInfo"),
                "Listening": lambda m: self.count_type(m, "Listening"),
                "Informed": lambda m: self.count_type(m, "Informed"),
            }
        )

        # Create Agents
        for (contents, x, y) in self.grid.coord_iter():
            if self.random.random() < density:

                agent = InfoAgent((x, y), self, self.spread_chance)

                # Set all agents in the first column to listening.
                if x == 0 and y == 0:
                    agent.condition = "Listening"
                
                self.grid.place_agent(agent, (x, y))
                self.schedule.add(agent)
        
        # # Infect some nodes
        # infected_nodes = self.random.sample(list(self.G), self.initial_outbreak_size)
        # for a in self.grid.get_cell_list_contents(infected_nodes):
        #     a.state = State.INFECTED

        self.running = True
        self.datacollector.collect(self)

    def step(self):
        self.schedule.step()
        # collect data
        self.datacollector.collect(self)

        # Halt if no more info
        if self.count_type(self, "Listening") == 0:
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


COLORS = {"NoInfo": "#FF9999", "Listening": "#9999FF", "Informed": "#00AA00"}

def canvas_config(agent):
    """
    Portrayal Method for canvas
    """
    if agent is None:
        return
    portrayal = {"Shape": "circle", "r": 0.5, "Filled": "true", "Layer": 0}
    (x, y) = agent.pos
    portrayal["x"] = x
    portrayal["y"] = y
    portrayal["Color"] = COLORS[agent.condition]
    return portrayal

def get_informed_agents(model):
    """ Display a text count of how many informed agents there are. """
    return f"Informed agents: {InfoModel.count_type(model, 'Informed')}"

print("h " + str(InfoModel.height))
canvas_element = mesa.visualization.CanvasGrid(
    # Grid Size (canvas) is equal and adjusts accordingly to the number of agents 
    canvas_config, InfoModel.height, InfoModel.width, 500, 500
)
graph_chart = mesa.visualization.ChartModule(
    [{"Label": label, "Color": color} for (label, color) in COLORS.items()]
)
pie_chart = mesa.visualization.PieChartModule(
    [{"Label": label, "Color": color} for (label, color) in COLORS.items()]
)

model_params = {
    "num_nodes": mesa.visualization.Slider("Number of Agents", 10, 10, 100, 1),
    "density": mesa.visualization.Slider("Agent density", 0.65, 0.01, 1.0, 0.01),
    "initial_outbreak": mesa.visualization.Slider("Initial Outbreak", 1, 1, 10, 1),
    "spread_chance": mesa.visualization.Slider("Spread Chance", 0.0, 0.0, 1.0, 0.1),
    "misinfo_chance": mesa.visualization.Slider("Misinformation Chance", 0.4, 0.0, 1.0, 0.1),
    "police_chance": mesa.visualization.Slider("Police Chance", 0.0, 0.0, 1.0, 0.1),
}

server = mesa.visualization.ModularServer(
    InfoModel, [canvas_element, get_informed_agents, graph_chart, pie_chart], "Information Spreading", model_params
)

   
