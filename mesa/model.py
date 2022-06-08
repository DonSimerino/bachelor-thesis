from mesa.space import SingleGrid
from mesa.time import RandomActivation
from mesa.datacollection import DataCollector


class SchellingAgent(Agent):
    # 1 Initialization
    def __init__(self, pos, model, agent_type):
        super().__init__(pos, model)
        self.pos = pos
        self.type = agent_type

    # 2 Step function
    def step(self):
        similar = 0
        # 3 Calculate the number of similar neighbours
        for neighbor in self.model.grid.neighbor_iter(self.pos):
            if neighbor.type == self.type:
                similar += 1

        # 4 Move to a random empty location if unhappy
        if similar < self.model.homophily:
            self.model.grid.move_to_empty(self)
        else:
            self.model.happy += 1


class Schelling(Model):
    def __init__():
      self.height = height
      self.width = width
      self.density = density
      self.minority_pc = minority_pc
      self.homophily = homophily

      self.grid = SingleGrid(height, width, torus=True)
      self.schedule = RandomActivation(self)
      self.happy = 0
      self.datacollector = DataCollector(                                   {"happy": "happy"},
      {"x": lambda a: a.pos[0], "y": lambda a: a.pos[1]}
      )

      for cell in self.grid.coord_iter():
        x = cell[1]
        y = cell[2]
        if self.random.random() < self.density:
          if self.random.random() < self.minority_pc:
            agent_type = 1
          else:
            agent_type = 0

          agent = SchellingAgent((x, y), self, agent_type)
          self.grid.position_agent(agent, (x, y))
          self.schedule.add(agent)

      self.running = True   
      self.datacollector.collect(self)


    def step(self):
      self.happy = 0  # 1 Reset counter of happy agents
      self.schedule.step()
      # 2 collect data
      self.datacollector.collect(self)

      # 3 Stop the model if all agents are happy
      if self.happy == self.schedule.get_agent_count():
        self.running = False