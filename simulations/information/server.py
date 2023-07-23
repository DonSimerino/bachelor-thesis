import mesa
from model import InfoModel
import matplotlib.pyplot as plt 
from matplotlib import colors
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

    # Plotting
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


def plot_failed_run(locations,states):
    # Create a 25x25 grid
    grid = np.zeros((25, 25))

    # Map states to colors
    state_codes = {
        'Informed': 1,
        'Disseminative': 1,
        'Unaware': 2,
        'Exhausted': 3
    }
    # Assign states to the corresponding cells
    for (x, y), state in zip(locations, states):
        grid[y][x] = state_codes[state]

    # Create a colormap for coloring the cells
    cmap = plt.cm.colors.ListedColormap(['white', 'green', 'red', 'purple'])

    # Plot the grid
    plt.figure(figsize=(8, 8))  # You can adjust the figure size as needed
    plt.imshow(grid, cmap=cmap, origin='lower', extent=[0, 25, 0, 25])

    # Add grid lines and labels for each cell
    plt.grid(which='both', color='black', linewidth=1)
    plt.xticks(range(25))
    plt.yticks(range(25))
    plt.xlim(0, 25)
    plt.ylim(0, 25)

    # Show the plot
    plt.show()




def run_simulation(iterations, starters, personality, conf, siren):
    # Start Evaluation 
    data = []
    failed_runs = 0
    
    locations =  [(0, 0), (0, 1), (0, 3), (0, 4), (0, 6), (0, 8), (0, 10), (0, 12), (0, 13), (0, 14), (0, 16), (0, 17), (0, 18), (0, 20), (0, 22), (0, 23), (0, 24), (1, 0), (1, 1), (1, 2), (1, 3), (1, 6), (1, 8), (1, 9), (1, 10), (1, 13), (1, 14), (1, 15), (1, 16), (1, 17), (1, 19), (1, 20), (1, 21), (1, 23), (1, 24), (2, 0), (2, 3), (2, 6), (2, 7), (2, 8), (2, 11), (2, 12), (2, 14), (2, 15), (2, 16), (2, 18), (2, 19), (2, 22), (2, 23), (3, 0), (3, 1), (3, 2), (3, 4), (3, 5), (3, 10), (3, 11), (3, 12), (3, 14), (3, 15), (3, 16), (3, 20),
                (3, 22), (4, 0), (4, 1), (4, 3), (4, 4), (4, 5), (4, 7), (4, 8), (4, 9), (4, 10), (4, 11), (4, 14), (4, 15), (4, 16), (4, 17), (4, 19), (4, 22), (5, 1), (5, 3), (5, 5), (5, 7), (5, 8), (5, 9), (5, 10), (5, 11), (5, 15), (5, 16), (5, 18), (5, 19), (5, 20), (5, 21), (5, 22), (5, 23), (5, 24), (6, 0), (6, 1), (6, 2), (6, 5), (6, 7), (6, 8), (6, 10), (6, 12), (6, 13), (6, 16), (6, 17), (6, 18), (6, 20), (6, 21), (6, 23), (6, 24), (7, 0), (7, 1), (7, 2), (7, 3), (7, 4), (7, 5), (7, 6), (7, 7), (7, 8), (7, 9), (7, 10), (7, 14), (7, 16), (7, 17), (7, 19), (7, 21), (7, 22), (7, 23), (7, 24), (8, 0), (8, 2), (8, 3), (8, 6), (8, 7), (8, 8), (8, 9), (8, 11), (8, 12), (8, 14), (8, 16), (8, 17), (8, 19), (8, 22), (9, 0), (9, 3), (9, 4), (9, 6), (9, 7), (9, 8), (9, 11), (9, 12), (9, 13), (9, 14), (9, 15), (9, 16), (9, 17), (9, 18), (9, 21), (9, 22), (9, 23), (10, 0), (10, 1), (10, 2), (10, 3), (10, 4), (10, 6), (10, 7), (10, 8), (10, 9), (10, 12), (10, 14), (10, 16), (10, 17), (10, 18), (10, 20), (10, 22), (10, 24), (11, 0), (11, 1), (11, 2), (11, 4), (11, 6), (11, 8), (11, 9), (11, 11), (11, 14), (11, 16), (11, 18), (11, 19), (11, 20), (11, 22), (11, 24), (12, 1), (12, 2), (12, 3), (12, 4), (12, 5), (12, 6), (12, 7), (12, 9), (12, 10), (12, 12), (12, 13), (12, 15), (12, 18), (12, 19), (12, 20), (12, 21), (12, 24), (13, 0), (13, 1), (13, 2), (13, 3), (13, 4), (13, 5), (13, 6), (13, 7), (13, 8), (13, 10), (13, 11), (13, 12), (13, 13), (13, 14), (13, 15), (13, 16), (13, 17), (13, 18), (13, 20), (13, 22), (13, 23), (13, 24), (14, 0), (14, 2), (14, 5), (14, 7), (14, 8), (14, 11), (14, 14), (14, 15), (14, 17), (14, 19), (14, 20), (14, 21), (14, 22), (14, 23), (14, 24), (15, 0), (15, 1), (15, 2), (15, 3), (15, 4), (15, 8), (15, 9), (15, 11), (15, 13), (15, 15), (15, 16), (15, 18), (15, 19), (15, 21), (15, 24), (16, 0), (16, 1), (16, 2), (16, 3), (16, 4), (16, 5), (16, 6), (16, 9), (16, 10), (16, 11), (16, 13), (16, 14), (16, 15), (16, 16), (16, 17), (16, 18), (16, 20), (16, 22), (16, 23), (16, 24), (17, 1), (17, 2), (17, 3), (17, 4), (17, 5), (17, 6), (17, 9), (17, 10), (17, 12), (17, 13), (17, 14), (17, 15), (17, 16), (17, 17), (17, 19), (17, 20), (17, 21), (17, 23), (18, 0), (18, 1), (18, 4), (18, 6), (18, 7), (18, 8), (18, 9), (18, 10), (18, 11), (18, 14), (18, 15), (18, 17), (18, 18), (18, 20), (18, 21), (18, 24), (19, 0), (19, 1), (19, 2), (19, 3), (19, 5), (19, 6), (19, 7), (19, 8), (19, 9), (19, 10), (19, 11), (19, 12), (19, 13), (19, 15), (19, 17), (19, 19), (19, 21), (19, 24), (20, 0), (20, 1), (20, 2), (20, 6), (20, 7), (20, 8), (20, 9), (20, 10), (20, 11), (20, 12), (20, 14), (20, 15), (20, 18), (20, 22), (20, 24), (21, 0), (21, 1), (21, 3), (21, 4), (21, 5), (21, 6), (21, 8), (21, 9), (21, 12), (21, 15), (21, 19), (21, 20), (21, 21), (21, 22), (21, 23), (22, 1), (22, 4), (22, 5), (22, 7), (22, 8), (22, 10), (22, 11), (22, 12), (22, 14), (22, 15), (22, 16), (22, 18), (22, 19), (22, 21), (22, 22), (22, 23), (23, 0), (23, 1), (23, 2), (23, 3), (23, 5), (23, 8), (23, 11), (23, 12), (23, 13), (23, 15), (23, 18), (23, 19), (23, 20), (23, 21), (23, 22), (23, 23), (23, 24), (24, 0), (24, 2), (24, 5), (24, 6), (24, 7), (24, 10), (24, 14), (24, 15), (24, 18), (24, 19), (24, 21), (24, 24)]


    for _ in range(iterations):
        model = InfoModel(0.65, starters, personality, conf, siren)
        step_count = 0
        temp_steps = []
        temp_informed = []

        previous_count = 0
        unchanged_count = 0

        while model.count_type(model, "Unaware") != 0:
            informed = 0
            model.step()

            for agent in model.schedule.agents:
                if agent.condition == "Informed" or agent.condition == "Disseminative":
                    informed += 1

            temp_steps.append(step_count)
            temp_informed.append(informed)
            step_count += 1

            # Check if the number of disseminative or informed agents has changed
            if informed == previous_count:
                unchanged_count += 1
            else:
                unchanged_count = 0
                previous_count = informed

            # Check if the number of agents hasn't changed for 15 steps
            if unchanged_count == 15:
                print("Breakpoint: Number of disseminative or informed agents hasn't changed in 5 steps.")
                break


  
  
        # Check if the simulation ran successfully (no unaware agents left)
        if model.count_type(model, "Unaware") == 0:
            data.append((temp_steps, temp_informed))
        else:
            # print(f"Simulation {_} discarded: Unaware agents remaining.")
            failed_runs += 1
            states = []
            
            for agent in model.grid.get_cell_list_contents(locations):
                states.append(agent.condition)

            plot_failed_run(locations, states)



    return data, failed_runs

# agent_choices = ["Confident", "Reserved", "Resilient", "Undercontrolled", "Overcontrolled", "Heterogeneous"]






# # # Run the simulation
data,failed_runs = run_simulation(iterations=10, starters=9, personality="Heterogeneous", conf="65", siren=False)
# # data_2,failed_runs_2 = run_simulation(iterations=1000, starters=1, personality="Confident", conf="80", siren=False)
# # data_3,failed_runs_3 = run_simulation(iterations=1000, starters=1, personality="Reserved", conf="80", siren=False)
# # data_4,failed_runs_4 = run_simulation(iterations=1000, starters=1, personality="Resilient", conf="80", siren=False)
# # data_5, failed_runs_5 = run_simulation(iterations=1000, starters=1, personality="Undercontrolled", conf="80", siren=False)
# # data_6, failed_runs_6 = run_simulation(iterations=1000, starters=1, personality="Overcontrolled", conf="80", siren=False)




# # Calculate and print the average of all time steps, growth rates and other infos
# avg_time_steps = int(calc_avg_time_steps(data))
# average_growth_rate = calc_average_growth_rate(data)

# # print(f"1: {failed_runs}")
# # print(f"2: {failed_runs_2}")
# # print(f"3: {failed_runs_3}")
# # print(f"4: {failed_runs_4}")
# # print(f"5: {failed_runs_5}")
# # print(f"6: {failed_runs_6}")

# # average_growth_rate_2 = calc_average_growth_rate(data_2)
# # average_growth_rate_3 = calc_average_growth_rate(data_3)
# # average_growth_rate_4 = calc_average_growth_rate(data_4)
# # average_growth_rate_5 = calc_average_growth_rate(data_5)
# # average_growth_rate_6 = calc_average_growth_rate(data_6)
# # print(average_growth_rate_2)
# # print(average_growth_rate_3)
# # print(average_growth_rate_4)
# # print(average_growth_rate_5)
# # print(average_growth_rate_6)

# # plt.plot([0,1], [0, average_growth_rate], label= "Heterogeneous")
# # plt.plot([0,1], [0, average_growth_rate_2], label= "Confident")
# # plt.plot([0,1], [0, average_growth_rate_3], label= "Reserved")
# # plt.plot([0,1], [0, average_growth_rate_4], label= "Resilient")
# # plt.plot([0,1], [0, average_growth_rate_5], label= "Undercontrolled")
# # plt.plot([0,1], [0, average_growth_rate_6], label= "Overcontrolled")

# # plt.ylabel("Informed Agents per step")
# # plt.xlabel("Simulation Time (steps)")
# # plt.title("Results over Iterations")
# # plt.legend()
# # plt.show()


# min_simulation_time = max(min(t[0] for t in data))
# max_simulation_time = max(max(t[0] for t in data))

# print(f"avg_time_steps: {avg_time_steps}")
# print(f"average_growth_rate: {average_growth_rate}")
# print("min_simulation_time:", min_simulation_time)
# print("max_simulation_time:", max_simulation_time)
# print(f"failed_runs: {failed_runs}")

# # Cut off all elements that exceed the array size of the average time steps 
# trimmed_data = [(t[0][:avg_time_steps], t[1][:avg_time_steps]) for t in data]

# # Ensure all tuples in trimmed_data have the same length
# min_length = min(len(t[1]) for t in trimmed_data)
# trimmed_data = [(t[0][:min_length], t[1][:min_length]) for t in trimmed_data]

# # Calculate the average growth curve
# avg_growth_curve = []
# for i in range(min_length):
#     avg_agents = sum(t[1][i] for t in trimmed_data) / len(trimmed_data)
#     avg_growth_curve.append(avg_agents)



# ### PLOTTING ###
# # Plot all simulation graphs
# for i, (temp_steps, temp_informed) in enumerate(trimmed_data):
#     plt.plot(temp_steps, temp_informed, alpha=0.2, color='blue')

# # Plot the average growth curve
# plt.plot(trimmed_data[0][0], avg_growth_curve, color='red', label='Average Distribution')

# # plt.plot(np.array(0), np.array(0), color='white', label=f'avg_time_steps {avg_time_steps}')
# # plt.plot(np.array(0), np.array(0), color='white', label=f'average_growth_rate {average_growth_rate}')

# plt.ylabel("Number of agents")
# plt.xlabel("Simulation Time (steps)")
# plt.title("Results over Iterations")
# plt.legend()
# plt.show()

