import mesa

class Dust(mesa.Agent):
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.state = "Dust"

class Vacuum(mesa.Agent):

    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.state = "Limpiando"
        self.moves = 0
    
    def move(self):
        steps = self.model.grid.get_neighborhood(self.pos, moore=True, include_center=False)
        position = self.random.choice(steps)
        self.model.grid.move_agent(self, position)
        self.moves += 1

    def step(self):
        self.move()

        cellmates = self.model.grid.get_cell_list_contents([self.pos])
        if any(isinstance(agent, Dust) for agent in cellmates):
            dirt = next(
                agent for agent in cellmates if isinstance(agent, Dust))
            self.state = "Limpiando"
            self.model.grid.remove_agent(dirt)

        else:
            self.state = "Reubicando"

class Map(mesa.Model):
    
    def __init__(self, width:int, height, agents_num: int, dustyCells, max_steps=100):
        self.schedule = mesa.time.RandomActivation(self)
        self.finished = False
        self.grid = mesa.space.MultiGrid(width, height, True)
        self.agents = agents_num
        self.max_steps = max_steps

        space = width * height

        dustyCells = space * dustyCells / 100

        for i in range(agents_num):
            a = Vacuum(i, self)
            self.schedule.add(a)
            self.grid.place_agent(a, (1, 1))

        i = 0
        while i < dustyCells:
            x = self.random.randrange(self.grid.width)
            y = self.random.randrange(self.grid.height)
            if self.grid.is_cell_empty((x, y)):
                dirt = Dust((x, y), self)
                self.grid.place_agent(dirt, (x, y))
                i += 1
        
        self.dusty_time = mesa.DataCollector(
            {
                "Dusty cells": self.dust_cells,
            }
        )

        self.clean_percentage = mesa.DataCollector(
            {
                "Clean percentage": self.clean_cells_percentage,
            }
        )

        self.total_moves = mesa.DataCollector(
            {
                "Total moves": self.total_moves_number,
            }
        )
        self.dusty_time.collect(self)
        self.clean_percentage.collect(self)
        self.total_moves.collect(self)

    def step(self):
        if self.schedule.steps >= self.max_steps:
            self.finished = True
        elif self.schedule.steps < self.max_steps:
            if self.dust_cells() == 0:
                self.finished = True
            else:
                self.schedule.step()
        self.clean_percentage.collect(self)
        self.dusty_time.collect(self)
        self.total_moves.collect(self)


    def run_model(self):
        while not self.finished:
            self.step()

    def dust_cells(self):
        dusty_cells = 0
        for cell in self.grid.coord_iter():
            cell_content, x, y = cell
            if any(isinstance(agent, Dust) for agent in cell_content):
                dusty_cells += 1
        return dusty_cells

    def dust_percentage(self):
        return self.dust_cells() / (self.grid.width * self.grid.height)*100
    
    def clean_cells_percentage(self):
        return self.clean_cells() / (self.grid.width * self.grid.height) *100

    def clean_cells(self):
        clean_cells = 0
        for cell in self.grid.coord_iter():
            cell_content, x, y = cell
            if not any(isinstance(agent, Dust) for agent in cell_content):
                clean_cells += 1
        return clean_cells

    def total_moves_number(self):
        moves = 0
        for agent in self.schedule.agents:
            moves += agent.moves
        return moves
