from Aspiradora import Map
import mesa


def agent_portrayal(agent):
    portrayal = {
        "Shape": "circle",
        "Filled": "true",
        "Layer": 0,
        "Color": "red",
        "r": 0.5,
    }

    if agent.state == "Dust":
        portrayal["Color"] = "grey"
    elif agent.state == "Limpiando":
        portrayal["Color"] = "green"
    else:
        portrayal["Color"] = "green"
    return portrayal


size = 10
dustyCells = 50
agents_num = 5

grid = mesa.visualization.CanvasGrid(agent_portrayal, size, size, 500, 500)

chart = mesa.visualization.ChartModule(
    [{"Label": "Dusty cells", "Color": "Black", }], data_collector_name="dusty_time"
)
chart2 = mesa.visualization.ChartModule(
    [{"Label": "Clean percentage", "Color": "Red" }], data_collector_name="clean_percentage"
)
chart3 = mesa.visualization.ChartModule(
    [{"Label": "Total moves", "Color": "blue" }], data_collector_name="total_moves"
)
print(chart2)
server = mesa.visualization.ModularServer(
    Map,
    [grid, chart, chart2, chart3],
    "Habitación",
    {"agents_num": agents_num, "width": size, "height": size, "dustyCells": dustyCells},
)

server.port = 8521
server.launch()
