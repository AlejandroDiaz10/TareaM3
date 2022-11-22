# Alejandro Díaz Villagómez - A01276769
# Fecha - 18/Noviembre/2022
# Simulación de una intersección

from mesa.visualization.ModularVisualization import ModularServer
from mesa.visualization.modules import CanvasGrid, ChartModule

#from CleaningModel import CleaningModel
from StreetModel import *


def agent_portrayal(agent):
    portrayal = {
        "Shape": "rect",
        "w": 1,
        "h": 1,
        "Filled": "true",
        "Layer": 0
    }
    # Calle
    if agent.unique_id > 1000 and agent.unique_id < 2000:
        portrayal["Color"] = "grey"

    # Pasto
    elif agent.unique_id > 2000:
        portrayal["Color"] = "green"

    # Semáforos
    elif agent.unique_id < 5:
        if agent.state == 0:
            portrayal["Color"] = "red"
        if agent.state == 1:
            portrayal["Color"] = "yellow"
        if agent.state == 2:
            portrayal["Color"] = "green"

    # Carros
    else:
        portrayal["Shape"] = "circle"
        portrayal["r"] = 0.8
        portrayal["Color"] = "black"

    return portrayal


grid = CanvasGrid(
    agent_portrayal,
    21,
    21,
    600,
    600
)

# Contador de coches que pasan
chart_counting_cars = ChartModule([{
    'Label': 'Counting_Cars',
    'Color': 'Black'}],
    data_collector_name='datacollector',
    canvas_height=40,
    canvas_width=80)

# Accidentes reportados
chart_car_crashes = ChartModule([{
    'Label': 'Car_Crashes',
    'Color': 'Black'}],
    data_collector_name='datacollector',
    canvas_height=40,
    canvas_width=80)

# Inicializamos el Modelo
#model_params = {"N": 4, "width": 21, "height": 21}
model_params = {"N": 6, "width": 21, "height": 21}

# Elementos que se mostrarán en el servidor
server = ModularServer(
    StreetModel,
    [grid, chart_counting_cars, chart_car_crashes],
    "Intersection Model",
    model_params
)

server.port = 8521
server.launch()
