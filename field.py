from cell import Cell

class Field:
    _field=[[]]

    def __init__(self, _field=[[]]):
        self._field = [[Cell(i, j, cell, canVisit=cell != 0) for j, cell in enumerate(row)] for i, row in enumerate(_field)]
        
    def position_in_bound(self, row, column):
        return row >= 0 and row < len(self._field) and column >= 0 and column < len(self._field[0])

    def get_cell(self, row, column):
        return self._field[row][column]
    
    def set_value(self, row, column, value):
        self._field[row][column].value = value
    
    def copy(self):
        field_copy = Field()
        field = self._field
        field_copy._field = [[cell.copy() for cell in row] for row in field]
        return field_copy