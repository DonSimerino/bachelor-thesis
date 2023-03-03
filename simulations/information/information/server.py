import mesa
import matplotlib.pyplot as plt
import numpy as np
#import ipdb  ipdb.set_trace()
from .model import InfoModel
import random

def test():
    # model = InfoModel(50,10,10)
    # for i in range(100):
    #     model.step()
    
    # gini = model.datacollector.get_model_vars_dataframe()
    # gini.plot()
    # plt.show()
    COLORS = {"NoInfo": "#00AA00", "Listening": "#880000", "Informed": "#000000"}


    def forest_fire_portrayal(tree):
        if tree is None:
            return
        portrayal = {"Shape": "rect", "w": 1, "h": 1, "Filled": "true", "Layer": 0}
        (x, y) = tree.pos
        portrayal["x"] = x
        portrayal["y"] = y
        portrayal["Color"] = COLORS[tree.condition]
        return portrayal


    canvas_element = mesa.visualization.CanvasGrid(
        forest_fire_portrayal, 100, 100, 500, 500
    )
    tree_chart = mesa.visualization.ChartModule(
        [{"Label": label, "Color": color} for (label, color) in COLORS.items()]
    )
    pie_chart = mesa.visualization.PieChartModule(
        [{"Label": label, "Color": color} for (label, color) in COLORS.items()]
    )

    model_params = {
        "height": 100,
        "width": 100,
        "density": mesa.visualization.Slider("Agent density", 0.65, 0.01, 1.0, 0.01),
    }
    server = mesa.visualization.ModularServer(
        InfoModel, [canvas_element, tree_chart, pie_chart], "Information Spreading", model_params
    )

    server.launch()
