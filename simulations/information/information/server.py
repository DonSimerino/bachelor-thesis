import mesa
import mesa.visualization.modules as mevisual
from mesa.visualization.UserParam import Slider
from mesa.visualization.ModularVisualization import ModularServer

from .model import InfoModel

def test():
    COLORS = {"NoInfo": "#00AA00", "Listening": "#880000", "Informed": "#000000"}


    def forest_fire_portrayal(agent):
        if agent is None:
            return
        portrayal = {"Shape": "rect", "w": 1, "h": 1, "Filled": "true", "Layer": 0}
        (x, y) = agent.pos
        portrayal["x"] = x
        portrayal["y"] = y
        portrayal["Color"] = COLORS[agent.condition]
        return portrayal


    canvas_element = mevisual.CanvasGrid(
        forest_fire_portrayal, 100, 100, 500, 500
    )
    tree_chart = mevisual.ChartModule(
        [{"Label": label, "Color": color} for (label, color) in COLORS.items()]
    )
    pie_chart = mevisual.PieChartModule(
        [{"Label": label, "Color": color} for (label, color) in COLORS.items()]
    )

    model_params = {
        "height": 100,
        "width": 100,
        "density": Slider("Agent density", 0.65, 0.01, 1.0, 0.01),
    }
    server = ModularServer(
        InfoModel, [canvas_element, tree_chart, pie_chart], "Information Spreading", model_params
    )

    server.launch()
