class Cell:
    isVisited = False
    canVisit = False

    def __init__(self, canVisit, row, column, stepCost = 1, distance=float('inf'), previous = None):
        self.canVisit = canVisit
        self.row = row
        self.column = column
        self.distance = distance
        self.stepCost = stepCost
        self.position = (row, column)
        self.previous = previous
    
    def __lt__(self, other):
        # Сравниваем клетки по расстоянию
        return self.distance < other.distance

class Field:
    field=[[]]

    def __init__(self, field):
        self.field = [[Cell(cell != 0, i, j, cell) for j, cell in enumerate(row)] for i, row in enumerate(field)]
        
    def position_in_bound(self, row, column):
        return row >= 0 and row < len(self.field) and column >= 0 and column < len(self.field[0])

    def get_cell(self, row, column):
        return self.field[row][column]
    
    def set_value(self, row, column, value):
        self.field[row, column].value = value
