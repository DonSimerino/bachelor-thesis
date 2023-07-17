import mesa
from model import InfoModel
import matplotlib.pyplot as plt 
import numpy as np
from collections import Counter






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


####################
# MODEL EVALUATION #
####################


def calc_avg_time_steps(data):
    return sum(len(t[0]) for t in data) / len(data)

def calc_average_growth_rate(data):
    # Calculate the average number of agents added per time step for each tuple
    avg_agents_per_step = []
    for t in data:
        time_steps = len(t[0])
        agents_added = t[1][-1] - t[1][0]  # Calculate the difference between the last and first agent count
        avg_agents = agents_added / time_steps
        avg_agents_per_step.append(avg_agents)

    average_growth_rate =  sum(avg_agents for i, avg_agents in enumerate(avg_agents_per_step, start=1)) / len(data)

    # # Plotting
    # for i, avg_agents in enumerate(avg_agents_per_step, start=1):
    #     plt.plot([0, 1], [0, avg_agents], alpha=0.2, color='blue')

    # plt.plot([0,1], [0, average_growth_rate], color='red', label='Average Growth Rate')
    # plt.plot(np.array(0), np.array(0), color='white', label=f'{"%.2f" % average_growth_rate} Agents per Step')
    # plt.ylabel("Informed Agents per step")
    # plt.xlabel("Simulation Time (steps)")
    # plt.title("Results over Iterations")
    # plt.legend()
    # plt.show()

    return average_growth_rate


def run_simulation(iterations, conf):
    # Start Evaluation 
    data = []

    for _ in range(iterations):
        model = InfoModel(0.65, 1, "Heterogeneous", conf, False)
        step_count = 0
        temp_steps = []
        temp_informed = []

        while model.count_type(model, "Unaware") != 0:
            informed = 0
            model.step()

            for agent in model.schedule.agents:
                if agent.condition == "Informed" or agent.condition == "Disseminative":
                    informed += 1

            temp_steps.append(step_count)
            temp_informed.append(informed)
            step_count += 1

        data.append((temp_steps,temp_informed))
    print(_)

    return data




# Run the simulation
data = run_simulation(iterations=10, conf="65%")



# Calculate and print the average of all time steps, growth rates and other infos
avg_time_steps = int(calc_avg_time_steps(data))
average_growth_rate = calc_average_growth_rate(data)
min_simulation_time = max(min(t[0] for t in data))
max_simulation_time = max(max(t[0] for t in data))

print(f"avg_time_steps: {avg_time_steps}")
print(f"average_growth_rate: {average_growth_rate}")
print("min_simulation_time:", min_simulation_time)
print("max_simulation_time:", max_simulation_time)

# Cut off all elements that exceed the array size of the average time steps 
trimmed_data = [(t[0][:avg_time_steps], t[1][:avg_time_steps]) for t in data]

# Ensure all tuples in trimmed_data have the same length
min_length = min(len(t[1]) for t in trimmed_data)
trimmed_data = [(t[0][:min_length], t[1][:min_length]) for t in trimmed_data]

# Calculate the average growth curve
avg_growth_curve = []
for i in range(min_length):
    avg_agents = sum(t[1][i] for t in trimmed_data) / len(trimmed_data)
    avg_growth_curve.append(avg_agents)



# Plot all simulation graphs
for i, (temp_steps, temp_informed) in enumerate(trimmed_data):
    plt.plot(temp_steps, temp_informed, alpha=0.2, color='blue')

# Plot the average growth curve
plt.plot(trimmed_data[0][0], avg_growth_curve, color='red', label='Average Distribution')


# plt.plot(np.array(0), np.array(0), color='white', label=f'avg_time_steps {avg_time_steps}')
# plt.plot(np.array(0), np.array(0), color='white', label=f'average_growth_rate {average_growth_rate}')

plt.ylabel("Number of agents")
plt.xlabel("Simulation Time (steps)")
plt.title("Results over Iterations")
plt.legend()
plt.show()

