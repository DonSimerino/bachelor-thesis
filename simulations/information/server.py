import mesa
from model import InfoModel


COLORS = {"Unaware": "#FF9999", "Informed": "#00AA00", "Disseminative": "#9E89FF", "Panic": "#800060", "Exhausted": "#808080"} # "Misinformed": "#800020"}

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

def get_total_agents(model):
    """ Display a text count of how many agents there are. """
    return f"Total agents: {InfoModel.count_all(model)}"

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

agent_choices = ["Confident", "Reserved", "Resilient", "Undercontrolled", "Overcontrolled", "Heterogeneous"]
message_choices = ["low - low", "high - high", "low - high", "high - low"]

model_params = {
    "_blankq_": mesa.visualization.StaticText("­"),

    "density": mesa.visualization.Slider("Agent density", 0.65, 0.01, 1.0, 0.01),
    "initial_outbreak": mesa.visualization.Slider("Initial Outbreak", 1, 1, 10, 1),

    "_blank_": mesa.visualization.StaticText("­"),
   
    "personality": mesa.visualization.Choice("Agents Personality", "Heterogeneous", agent_choices),
    "_blank2w_": mesa.visualization.StaticText("­"),

    "message" :mesa.visualization.Choice('Message: urgency - complexity', 'low - low', message_choices),
    "_blank_w": mesa.visualization.StaticText("­"),

    "include_sirens": mesa.visualization.Checkbox("Include Sirens", False),
    "_blank2_": mesa.visualization.StaticText("­"),
    
    "text": mesa.visualization.StaticText("To change the behaviour using the message, increase complexity for misinfo and urgency for spread rate."),

}

template = "frontend\template.html"

server = mesa.visualization.ModularServer(
    InfoModel, [canvas_element, get_informed_agents, get_total_agents, graph_chart, pie_chart], "Information Spreading", model_params
)

   
