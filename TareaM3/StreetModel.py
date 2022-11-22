# Alejandro Díaz Villagómez - A01276769
# Fecha - 18/Noviembre/2022
# Simulación de una intersección

from mesa import Model
from mesa.space import MultiGrid
from mesa.time import RandomActivation
from mesa.datacollection import DataCollector

from Agents import *


class StreetModel(Model):
    def __init__(self, N, width, height):
        self.num_agents = N
        self.running = True
        self.neighbors = False
        self.waiting_time = N*5
        self.crashes = 0
        self.counting_cars = 0

        # Espacio físico para los agentes
        # Permitimos que se salgan del mapa
        self.grid = MultiGrid(width, height, True)
        self.schedule = RandomActivation(self)
        self.running = True

        # Le damos color al grid
        id_cont = 1
        for i in range(width):
            for j in range(height):
                # Es una celda calle (sus IDs serán mayor a 1000)
                if (i > 7 and i < 13) or (j > 7 and j < 13):
                    id = 1000 + id_cont
                    a = Color(id, self)
                    self.schedule.add(a)
                    self.grid.place_agent(a, (i, j))
                # Es una celda pasto (sus IDs serán mayor a 2000)
                else:
                    id = 2000 + id_cont
                    a = Color(id, self)
                    self.schedule.add(a)
                    self.grid.place_agent(a, (i, j))
                id_cont += 1

        # Colocamos los semáforos
        coord_traffic = [(7, 9), (13, 11), (11, 7), (9, 13)]
        for i in range(0, len(coord_traffic)):
            traffic_light = TrafficLight(i + 1, self, 1)
            self.schedule.add(traffic_light)
            self.grid.place_agent(traffic_light, coord_traffic[i])

        # Colocamos los carros
        coord_cars = [(9, 15), (18, 11), (11, 2), (1, 9)]
        coord_cars_dir = [4, 2, 3, 1]
        for j in range(0, len(coord_cars)):
            car = Car(j + len(coord_traffic) + 1, self, coord_cars_dir[j])
            self.schedule.add(car)
            self.grid.place_agent(car, coord_cars[j])

        #Carros para mejorar la simulación
        c9 = Car(9, self, 4)
        self.schedule.add(c9)
        self.grid.place_agent(c9, (9, 1))
        c10 = Car(10, self, 1)
        self.schedule.add(c10)
        self.grid.place_agent(c10, (2, 9))

        #Carros para colisión
        # c15 = Car(15, self, 4)
        # self.schedule.add(c15)
        # self.grid.place_agent(c15, (9, 13))
        # c25 = Car(25, self, 2)
        # self.schedule.add(c25)
        # self.grid.place_agent(c25, (11, 11))

        # Metrics we will measure about our model
        self.datacollector = DataCollector(
            model_reporters={
                "Car_Crashes": compute_car_crashes,
                "Counting_Cars": compute_counting_cars
            },
        )

    def step(self):
        self.datacollector.collect(self)
        self.schedule.step()
        print(self.counting_cars)
    
    def run_model(self):
        while self.running:
            self.step()
