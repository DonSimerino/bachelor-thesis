import mesa


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

   
    # def step(self):
    #     if self.state is State.INFECTED:
    #         self.try_to_infect_neighbors()
    #     self.try_check_situation()


    def try_to_infect_neighbors(self):
        neighbors_nodes = self.model.grid.get_neighbors(self.pos, include_center=False)
        susceptible_neighbors = [
            agent
            for agent in self.model.grid.get_cell_list_contents(neighbors_nodes)
            if agent.state is State.SUSCEPTIBLE
        ]
        for a in susceptible_neighbors:
            if self.random.random() < self.spread_chance:
                a.state = State.INFECTED

    

