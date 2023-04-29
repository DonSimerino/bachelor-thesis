import mesa
from model import InfoModel


COLORS = {"NoInfo": "#FF9999", "Listening": "#9999FF", "Informed": "#00AA00", "Misinformed": "#800020"}

def canvas_config(agent):
    """ Portrayal Method for canvas """
    
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

def get_misinformed_agents(model):
    """ Display a text count of how many misinformed agents there are. """
    return f"Misinformed agents: {InfoModel.count_type(model, 'Misinformed')}"

canvas_element = mesa.visualization.CanvasGrid(
    # Grid Size (canvas) is equal and adjusts accordingly to the number of agents 
    canvas_config, InfoModel.height, InfoModel.width, 500, 500
)
graph_chart = mesa.visualization.ChartModule(
    [{"Label": label, "Color": color} for (label, color) in COLORS.items()]
)
pie_chart = mesa.visualization.PieChartModule(
    [{"Label": label, "Color": color} for (label, color) in COLORS.items()],
    #500, 500,  # adjust chart_height and chart_width as needed
)
agent_choices = ["Experts", "Followers", "Skeptics", "Social Butterflys", "Outlaws", "Default"]
message_choices = ["low - low", "high - high", "low - high", "high - low"]

model_params = {
    # "num_nodes": mesa.visualization.Slider("Number of Agents", 10, 10, 100, 1),
    "_blankq_": mesa.visualization.StaticText("­"),

    "density": mesa.visualization.Slider("Agent density", 0.65, 0.01, 1.0, 0.01),
    "initial_outbreak": mesa.visualization.Slider("Initial Outbreak", 1, 1, 10, 1),
    "misinfo_chance": mesa.visualization.Slider("Misinformation", 0, 0, 1.0, 0.1, description="Regulate the rate of misinformation."),

    # "experts": mesa.visualization.Slider("Experts", 0, 0, 1.0, 0.1,  description="high level in every category"),
    # "followers": mesa.visualization.Slider("Followers", 0, 0, 1.0, 0.1, description="low knowledge, confidence"),
    # "skeptic": mesa.visualization.Slider("Skeptic", 0, 0, 1.0, 0.1, description="low social, trust"),
    # "social_butterfly": mesa.visualization.Slider("Social Butterfly", 0, 0, 1.0, 0.1, description="low risk, knowledge"),
    # "outlaws": mesa.visualization.Slider("Outlaws", 0, 0, 1.0, 0.1, description="low level in every category"),

    "_blank_": mesa.visualization.StaticText("­"),
    
    "agents_personality": mesa.visualization.Choice("Agents Personality", "Default", agent_choices),
    "_blank2w_": mesa.visualization.StaticText("­"),

    "message" :mesa.visualization.Choice('Message: urgency - complexity', 'low - low', message_choices),

    "_blank_w": mesa.visualization.StaticText("­"),

    "include_sirens": mesa.visualization.Checkbox("Include Sirens", False),

    "_blank2_": mesa.visualization.StaticText("­"),
    
    "text": mesa.visualization.StaticText("To change the behaviour using the message, increase complexity for misinfo and urgency for spread rate."),

}

template = "frontend\template.html"

server = mesa.visualization.ModularServer(
    InfoModel, [canvas_element, get_informed_agents, get_misinformed_agents, graph_chart, pie_chart], "Information Spreading", model_params
)

   
