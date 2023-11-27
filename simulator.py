import networkx as nx
import matplotlib.pyplot as plt
import random
import ipywidgets as widgets
from IPython.display import display
import time

def initialize_graph(nodes, edges):
    G = nx.gnm_random_graph(nodes, edges)
    for node in G.nodes():
        G.nodes[node]['state'] = 'S'  # 'S' for susceptible
    patient_zero = random.choice(list(G.nodes()))
    G.nodes[patient_zero]['state'] = 'I'  # 'I' for infected
    return G

def plot_graph(G, day):
    plt.figure(figsize=(10, 8))

    pos = nx.spring_layout(G, seed=42)
    node_colors = {'S': 'blue', 'I': 'red', 'R': 'green', 'E': 'purple', 'V': 'yellow'}
    colors = [node_colors.get(G.nodes[node]['state'], 'white') for node in G.nodes()]

    # drawing nodes and edges 
    nx.draw_networkx_nodes(G, pos, node_size=200, node_color=colors)
    nx.draw_networkx_edges(G, pos, width=0.5)

    # labels
    legend_labels = {'Susceptible': 'blue', 'Infected': 'red', 'Recovered': 'green', 'Exposed': 'purple', 'Vaccinated': 'yellow'}
    legend_handles = [plt.Line2D([0], [0], marker='o', color=color, label=label, markersize=8, linestyle='None') for label, color in legend_labels.items()]
    plt.legend(handles=legend_handles, loc='upper right')

    plt.title(f"Epidemic Spread - Day {day}")
    plt.axis('off')

    plt.show()

def spread_epidemic(G, beta, gamma, sigma, vaccination_prob):
    new_G = G.copy()
    for node in G.nodes():
        if G.nodes[node]['state'] == 'I':
            for neighbor in G.neighbors(node):
                if G.nodes[neighbor]['state'] == 'S' and random.random() < beta:
                    new_G.nodes[neighbor]['state'] = 'E'  # 'E' for exposed
        elif G.nodes[node]['state'] == 'E' and random.random() < sigma:
            new_G.nodes[node]['state'] = 'I'  # Transition from exposed to infected
        elif G.nodes[node]['state'] == 'I' and random.random() < gamma:
            new_G.nodes[node]['state'] = 'R'  # 'R' for recovered
        elif G.nodes[node]['state'] == 'S' and random.random() < vaccination_prob:
            new_G.nodes[node]['state'] = 'V'  # 'V' for vaccinated
    return new_G

def simulate_epidemic(nodes, edges, beta, gamma, sigma, vaccination_prob, days):
    G = initialize_graph(nodes, edges)
    current_day = 1

    while current_day <= days:
        plot_graph(G, current_day)
        G = spread_epidemic(G, beta, gamma, sigma, vaccination_prob)
        current_day += 1
        time.sleep(0.5)

#sliders
style = {'description_width': 'initial'}
nodes_slider = widgets.IntSlider(value=50, min=10, max=100, step=5, description='Nodes:', style=style)
edges_slider = widgets.IntSlider(value=80, min=10, max=150, step=5, description='Edges:', style=style)
beta_slider = widgets.FloatSlider(value=0.3, min=0.1, max=0.5, step=0.05, description='Infection Rate:', style=style)
gamma_slider = widgets.FloatSlider(value=0.1, min=0.05, max=0.3, step=0.05, description='Recovery Rate:', style=style)
sigma_slider = widgets.FloatSlider(value=0.2, min=0.1, max=0.5, step=0.05, description='Incubation Rate:', style=style)
vaccination_slider = widgets.FloatSlider(value=0.1, min=0.0, max=1.0, step=0.1, description='Vaccination Probability:', style=style)
days_slider = widgets.IntSlider(value=10, min=5, max=30, step=1, description='Days:', style=style)

def run_simulation(button):
    simulate_epidemic(
        nodes_slider.value,
        edges_slider.value,
        beta_slider.value,
        gamma_slider.value,
        sigma_slider.value,
        vaccination_slider.value,
        days_slider.value
    )

run_button = widgets.Button(description="Run Simulation")
run_button.on_click(run_simulation)

display(nodes_slider, edges_slider, beta_slider, gamma_slider, sigma_slider, vaccination_slider, days_slider, run_button)


