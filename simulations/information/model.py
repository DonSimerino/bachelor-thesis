import mesa
from agent import InfoAgent
import random
import pdb

class InfoModel(mesa.Model):
    """A agent model with some number of agents"""
    
    height = 25 
    width = 25

    def __init__(
            self, 
            density,
            initial_outbreak,
            personality,
            message,
            include_sirens):

        self.density = density
        self.initial_outbreak = initial_outbreak
     
        self.personality = self.get_personality(personality.lower())

        self.include_sirens = include_sirens
        self.message = message

        self.schedule = mesa.time.RandomActivation(self)
        

        # Grid Size (agents) is equal and adjusts accordingly to the number of agents 
        self.grid = mesa.space.MultiGrid(self.height, self.width, torus=False)
        agent_locations = [(x,y) for (contents, x, y) in self.grid.coord_iter() if self.random.random() < density]


        self.datacollector = mesa.datacollection.DataCollector(
            {
                "Unaware": lambda m: self.count_type(m, "Unaware"),
                "Informed": lambda m: self.count_type(m, "Informed"),
                "Disseminative": lambda m: self.count_type(m, "Disseminative"),
                "Panic": lambda m: self.count_type(m, "Panic"),
                "Exhausted": lambda m: self.count_type(m, "Exhausted"),
            }
        )

        # Create Agents
        for (x,y) in agent_locations:
            agent = InfoAgent((x, y), self, self.personality, self.message)
  
            if self.include_sirens: # If you want all the corners to start.
                if (x,y) in [(0,0), (0,24), (24,0), (24,24)]:
                    agent.condition = "Informed"
                    agent.action_queue = [agent.try_disseminate]
            else: # This is the default start.
                if (x,y) == (0,0):
                    agent.condition = "Informed"
                    agent.action_queue = [agent.try_disseminate]
                
            self.grid.place_agent(agent, (x, y))
            self.schedule.add(agent)
 

        # Randomly infect some nodes
        for agent in self.sample_agents(agent_locations, self.initial_outbreak-1):
            agent.condition = "Informed"
            agent.action_queue = [agent.try_disseminate]


        # Heterogeneous agent distribution
        if personality.lower() == "heterogeneous":
            fractions = self.get_personality("heterogeneous")[1] 
            groups = list(fractions.keys())
            group_agents = {group: [] for group in groups}

            # Assign each agent to a group based on the fractions
            for agent in self.sample_agents(agent_locations,  len(agent_locations)):
                group = random.choices(groups, weights=list(fractions.values()))[0]
                group_agents[group].append(agent)

            # Assign each agent their respective personalty
            for group, agents in group_agents.items():
                for agent in agents:
                    agent.personality_name = group
                    agent.personality_values = self.get_personality(group)[1] 
                
                

        # # Test heterogeneous distribution
        # count_personality = {
        # 'confident': 0,
        # 'reserved': 0,
        # 'resilient': 0,
        # 'undercontrolled': 0,
        # 'overcontrolled': 0
        # }

        # for agent in self.grid.get_cell_list_contents(agent_locations):
        #     if agent.personality_name in count_personality:
        #         count_personality[agent.personality_name] += 1

        # for personality, count in count_personality.items():
        #     print(f"{personality}: {count}")


        self.running = True
        self.datacollector.collect(self)


    def step(self):
        self.schedule.step()
        # collect data
        self.datacollector.collect(self)
        # Halt if no more info
        if self.count_type(self, "Unaware") == 0: #and self.count_type(self, "Listening") == 0:
            self.running = False



# Helper functions

    def sample_agents(self, agent_locations, amount):
        return self.grid.get_cell_list_contents(self.random.sample(agent_locations, amount))

    def get_personality(self, type_name=None):
        personalities = {
            "confident": {'agreeableness': 0.5, 'openness': 0.6, 'conscientiousness': 0.5, 'extraversion': 0.6, 'neuroticism': 0.5},
            "reserved": {'agreeableness': 0.6, 'openness': 0.2, 'conscientiousness': 0.6, 'extraversion': 0.2, 'neuroticism': 0.2},
            "resilient": {'agreeableness': 0.8, 'openness': 0.4, 'conscientiousness': 0.8, 'extraversion': 0.8, 'neuroticism': 0.2},
            "undercontrolled": {'agreeableness': 0.2, 'openness': 0.4, 'conscientiousness': 0.2, 'extraversion': 0.4, 'neuroticism': 0.8},
            "overcontrolled": {'agreeableness': 0.3, 'openness': 0.3, 'conscientiousness': 0.4, 'extraversion': 0.2, 'neuroticism': 0.9},
            "heterogeneous": {'confident': 0.221, 'reserved': 0.2541, 'resilient': 0.1631, 'undercontrolled': 0.2401, 'overcontrolled': 0.1217}
        }
        return next((key, value) for key, value in personalities.items() if key == type_name)

      
    # Low: 0.2
    # Medium/Low: 0.3
    # Moderate: 0.4
    # Medium: 0.5
    # Moderately High/Positive: 0.6
    # Pronounced: 0.7
    # High: 0.8
    # pronounced: 0.9


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

    @staticmethod
    def count_all(model):
        """
        Helper method to count agents in a given condition in a given model.
        """
        count = 0
        for agent in model.schedule.agents:
            count += 1
        return count