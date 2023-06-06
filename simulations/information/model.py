import mesa
from agent import InfoAgent
import pdb

class InfoModel(mesa.Model):
    """A agent model with some number of agents"""
    
    height = 25 
    width = 25

    def __init__(
            self, 
            density,
            initial_outbreak,
            # experts,
            # followers,
            # skeptic,
            # social_butterfly,
            # outlaws,
            agents_personality,
            message,
            include_sirens,
            misinfo_chance):

        self.density = density
        self.initial_outbreak = initial_outbreak
        # self.experts= experts
        # self.followers= followers 
        # self.skeptic = skeptic 
        # self.social_butterfly = social_butterfly 
        # self.outlaws = outlaws  
        self.personality = self.get_personality(agents_personality.lower())
        self.include_sirens = include_sirens
        self.misinfo_chance = misinfo_chance
        self.message = message

        self.schedule = mesa.time.RandomActivation(self)
        

        # Grid Size (agents) is equal and adjusts accordingly to the number of agents 
        self.grid = mesa.space.MultiGrid(self.height, self.width, torus=False)
        agent_locations = [(x,y) for (contents, x, y) in self.grid.coord_iter() if self.random.random() < density]
        # personality_fractions = {"experts": self.experts, "followers": self.followers, "skeptics": self.skeptic, "social_butterflys": self.social_butterfly, "outlaws": self.outlaws}


        self.datacollector = mesa.datacollection.DataCollector(
            {
                "NoInfo": lambda m: self.count_type(m, "NoInfo"),
                "Listening": lambda m: self.count_type(m, "Listening"),
                "Informed": lambda m: self.count_type(m, "Informed"),
                "Misinformed": lambda m: self.count_type(m, "Misinformed"),
            }
        )

        # Create Agents
        for (x,y) in agent_locations:
            agent = InfoAgent((x, y), self, self.personality, self.message, self.misinfo_chance)
  
            if self.include_sirens: # If you want all the corners to start.
                if (x,y) in [(0,0), (0,24), (24,0), (24,24)]:
                    agent.condition = "Informed"
                    agent.action_queue = [agent.share_information]
            else: # This is the default start.
                if (x,y) == (0,0):
                    agent.condition = "Informed"
                    agent.action_queue = [agent.share_information]
                
            self.grid.place_agent(agent, (x, y))
            self.schedule.add(agent)
 

        # Randomly infect some nodes
        for agent in self.sample_agents(agent_locations, self.initial_outbreak-1):
            agent.condition = "Informed"
            agent.action_queue = [agent.share_information]
        # self.perform_action_on_sampled_agents(agent_locations, "condition", "Informed", self.initial_outbreak-1)



        # Randomly set nodes personality
        # TODO: bisher werden alle agenten auf die input personality gesetzt -> WIP fraction-personality-zuweisung 
        # personality_attrs =  self.get_agent_personality(self.agents_personality.lower())
        # for agent in self.get_agents_sample(agent_locations,  len(agent_locations)):
        #     agent.parameters = personality_attrs


        # for personality_name, fraction in personality_fractions.items():
        #     personality_attrs =  self.get_agent_personality(personality_name)
        #     self.perform_action_on_sampled_agents(agent_locations, "parameters", personality_attrs, len(agent_locations)*fraction)
        # self.perform_action_on_sampled_agents(agent_locations, "parameters", personality_attrs, len(agent_locations))

        self.running = True
        self.datacollector.collect(self)


    def step(self):
        self.schedule.step()
        # collect data
        self.datacollector.collect(self)
        # Halt if no more info
        if self.count_type(self, "NoInfo") == 0 and self.count_type(self, "Listening") == 0:
            self.running = False



    # def perform_action_on_sampled_agents(self, agent_locations, action, value, amount):
    #     try:
    #         # pdb.set_trace()  # set a breakpoint
    #         nodes = self.random.sample(agent_locations, int(amount))
    #         for a in self.grid.get_cell_list_contents(nodes):
    #             setattr(a, action, value)
    #     except Exception as e:
    #         print(f"An exception occurred while performing '{action}' '{value}' '{amount}' on agents: {e}")

    def sample_agents(self, agent_locations, amount):
        return self.grid.get_cell_list_contents(self.random.sample(agent_locations, amount))

    def get_personality(self, type_name=None):
        personalities = {
            "experts": {'sociality': 1, 'perceived_risk': 1, 'knowledge': 1, 'confidence': 1, 'trust': 1},
            "followers": {'sociality': 1, 'perceived_risk': .6667, 'knowledge': .3334, 'confidence': .3334, 'trust': 1},
            "skeptics": {'sociality': .3334, 'perceived_risk': 1, 'knowledge': 1, 'confidence': .6667, 'trust': .3334},
            "social_butterflys": {'sociality': 1, 'perceived_risk': .3334, 'knowledge': .3334, 'confidence': .6667, 'trust': 1},
            "outlaws": {'sociality': .3334, 'perceived_risk': .3334, 'knowledge': .3334, 'confidence': .3334, 'trust': .3334},
            "default": {'sociality': .5, 'perceived_risk': .5, 'knowledge': .5, 'confidence': .5, 'trust': .5}
        }
        if type_name is None:
            return personalities["default"]
        else:
            return personalities[type_name]


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
