# Alejandro Díaz Villagómez - A01276769
# Fecha - 18/Noviembre/2022
# Simulación de una intersección

from mesa import Agent

# Calculamos la cantidad de choques en el modelo
def compute_car_crashes(model):
    return model.crashes

# Calculamos la cantidad de carros que pasan por los semáforos
def compute_counting_cars(model):
    return model.counting_cars


# Usaremos este agente para colorear el grid
class Color(Agent):
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)


# Agente 1 - Carros
class Car(Agent):
    def __init__(self, unique_id, model, direction):
        super().__init__(unique_id, model)
        self.moving = True
        self.mov_dir = direction
        self.distance2tl = 10

    # ¿Qué pasará en cada unidad de tiempo?
    def step(self):
        if self.moving == True:
            self.move()

    # Función para movernos
    def move(self):
        x, y = self.pos
        # Hay 4 posibles direcciones: derecha(1), izquierda(2), arriba(3), abajo(4)
        if self.mov_dir == 1:
            if x + 1 >= 21:
                new_position = (0, y)
            else: 
                new_position = (x + 1, y)
            cellmates = self.model.grid.get_cell_list_contents([new_position])
            self.distance2tl = - x - 1 + 7
            # print("Carro: " + str(self.unique_id) +
            #       "\tDistancia: " + str(self.distance2tl))
        elif self.mov_dir == 2:
            new_position = (x - 1, y)
            cellmates = self.model.grid.get_cell_list_contents([new_position])
            self.distance2tl = x - 1 - 13
            # print("Carro: " + str(self.unique_id) +
            #       "\tDistancia: " + str(self.distance2tl))
        elif self.mov_dir == 3:
            if y + 1 >= 21:
                new_position = (x, 0)
            else: 
                new_position = (x, y + 1)
            cellmates = self.model.grid.get_cell_list_contents([new_position])
            self.distance2tl = - y - 1 + 7
            # print("Carro: " + str(self.unique_id) +
            #       "\tDistancia: " + str(self.distance2tl))
        else:
            new_position = (x, y - 1)
            cellmates = self.model.grid.get_cell_list_contents([new_position])
            self.distance2tl = y - 1 - 13
            # print("Carro: " + str(self.unique_id) +
            #       "\tDistancia: " + str(self.distance2tl))

        # Cada 5 pasos reseteamos el tiempo de espera
        # print("Model time: " + str(self.model.waiting_time))
        self.model.waiting_time -= 1
        
        #Hay un choque
        list_a = []
        for a in self.model.schedule.agents:
            if a.unique_id > 5 and a.unique_id < 100:
                list_a.append(a.unique_id)
                # print("Id: " + str(a.unique_id))
        
        noRepeatingElements = set(list_a)
        #Hubo un choque, es necesario reportarlo
        if len(noRepeatingElements) != len(list_a):
            self.model.crashes += 1


        if len(cellmates) > 1:
            for c in cellmates:
                #El semáforo está en verde y no se ha acabado el tiempo (Verde)
                if c.unique_id < 5 and c.pass_car == True and self.model.waiting_time > 0:
                    c.change_traffic_light(1)
                    self.model.grid.move_agent(self, new_position)
                    self.model.counting_cars += 1
                    # print("Passing")

                #El semáforo está en verde pero ya se acabó el tiempo (Rojo)
                if c.unique_id < 5 and c.pass_car == False and self.model.waiting_time <= 0:
                    c.change_traffic_light(2)
                    # print("Timeout")

                #Está en rojo el semáforo y un coche quiere pasar
                elif c.unique_id < 5 and c.pass_car == False:
                    c.change_traffic_light(3)
                    # print("Wait")

        #No hay semáforo, el coche puede avanzar
        else:
            self.model.grid.move_agent(self, new_position)

    
        

# Agente 2 - Semáforos
class TrafficLight(Agent):
    def __init__(self, unique_id, model, color):
        super().__init__(unique_id, model)
        # Hay tres estados: rojo(0), amarillo(1) y verde(2)
        self.state = color
        self.pass_car = False
        self.waiting_time = 5

    def change_traffic_light(self, case):
        #El semáforo está en verde y no se ha acabado el tiempo (Verde)
        if case == 1:
            self.model.waiting_time = 5 * self.model.num_agents
            self.state = 1
            # print("Case1 - Model time: " + str(self.model.waiting_time))

        #El semáforo está en verde pero ya se acabó el tiempo (Rojo)
        elif case == 2:
            self.reset_lights()
            self.model.waiting_time = 5 * self.model.num_agents
            self.pass_car = False
            # print("Case2 - Model time: " + str(self.model.waiting_time))

        #Está en rojo el semáforo y un coche quiere pasar
        elif case == 3:
            if self.isActive():
                # print("Is Active: " + str(self.model.waiting_time))
                pass
            else:
                self.pass_car = True
                self.state = 2
                self.change_color_red()
                # print("Case3 - Model time: " + str(self.model.waiting_time))


    def isActive(self):
        for agent in self.model.schedule.agents:
            if agent.unique_id < 5 and agent.pass_car == True:
                return True
        return False


    def reset_lights(self):
        for agent in self.model.schedule.agents:
            if agent.unique_id < 5 and agent.pass_car == True:
                agent.pass_car = False
                agent.state = 0
                return

    def change_color_red(self):
        for agent in self.model.schedule.agents:
            if agent.unique_id < 5 and agent.pass_car == False:
                agent.state = 0
    
    

