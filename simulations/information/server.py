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
    # "num_nodes": mesa.visualization.Slider("Number of Agents", 10, 10, 100, 1),
    "density": mesa.visualization.Slider("Agent density", 0.65, 0.01, 1.0, 0.01),
    "initial_outbreak": mesa.visualization.Slider("Initial Outbreak", 1, 1, 10, 1),
    "spread_chance": mesa.visualization.Slider("Spread Chance", 1, 0.1, 1.0, 0.1),
    "receive_chance": mesa.visualization.Slider("Receive Info Chance", 1, 0.1, 1.0, 0.1),
    "misinfo_chance": mesa.visualization.Slider("Misinformation Chance", 0.4, 0.0, 1.0, 0.1),
    "police_chance": mesa.visualization.Slider("Police Chance", 0.0, 0.0, 1.0, 0.1),
}

server = mesa.visualization.ModularServer(
    InfoModel, [canvas_element, get_informed_agents, graph_chart, pie_chart], "Information Spreading", model_params
)

   
