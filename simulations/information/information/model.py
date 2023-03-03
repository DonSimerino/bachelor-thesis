from mesa.time import RandomActivation
from mesa.space import Grid
from mesa import Model
from mesa.datacollection import DataCollector

from .agent import InfoAgent


class InfoModel(Model):
 
    def __init__(self, width=100, height=100, density=0.65):
        """
        Create a new agent info model.

        Args:
            width, height: The size of the grid to model
            density: What fraction of grid cells have a person in them.
        """
        self.schedule = RandomActivation(self)
        self.grid = Grid(width, height, torus=False)

        self.datacollector = DataCollector(
            {
                "NoInfo": lambda m: self.count_type(m, "NoInfo"),
                "Listening": lambda m: self.count_type(m, "Listening"),
                "Informed": lambda m: self.count_type(m, "Informed"),
            }
        )

        # Place a peron in each cell with Prob = density
        for (contents, x, y) in self.grid.coord_iter():
            if self.random.random() < density:
                # Create a person
                new_person = InfoAgent((x, y), self)

                # Set all agents in the first column to listening.
                if x == 0 and y == 0:
                    new_person.condition = "Listening"
                self.grid.place_agent(new_person, (x, y))
                self.schedule.add(new_person)

        self.running = True
        self.datacollector.collect(self)

            # 'create agents'
        # for i in range(self.num_agents):
        #     a = InfoAgent(i,self)
        #     self.schedule.add(a)
            
        #     #add agent to random cell
        #     x = self.random.randrange(self.grid.width)
        #     y = self.random.randrange(self.grid.height)
        #     self.grid.place_agent(a, (x,y))

        # self.datacollector = DataCollector(
        #     model_reporters={"Gini": compute_gini}, agent_reporters={"Wealth": "wealth"}
        # )

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
