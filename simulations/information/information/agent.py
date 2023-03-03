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

    def __init__(self, pos, model):
        """
        Create a new person.
        Args:
            pos: The perons's coordinates on the grid. (unique_id)
            model: standard model reference for agent.
        """
        super().__init__(pos, model)
        self.pos = pos
        self.condition = "NoInfo"

    def step(self):
        """
        If the person is listening, spread it to uninformed people nearby.
        """
        if self.condition == "Listening":
            for neighbor in self.model.grid.iter_neighbors(self.pos, True):
                if neighbor.condition == "NoInfo":
                    neighbor.condition = "Listening"
            self.condition = "Informed"

        # self.move()
        # if self.wealth > 0:
        #     self.give_money()

    
    def move(self):
        possible_steps = self.model.grid.get_neighborhood(
            self.pos,
            moore = True,
            include_center= False)
        new_position = self.random.choice(possible_steps)
        self.model.grid.move_agent(self, new_position)


    def give_money(self):
        cellmates = self.model.grid.get_cell_list_contents([self.pos])
        if len(cellmates) > 1:
            other_agent = self.random.choice(cellmates)
            other_agent.wealth += 1
            self.wealth -= 1


