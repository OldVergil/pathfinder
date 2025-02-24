from collections import deque
from queue import PriorityQueue

class Cell:
    isVisited = False
    canVisit = False

    def __init__(self, row, column, stepCost = 1, distance=float('inf'), previous = None, isVisited = False, canVisit = False):
        self.canVisit = canVisit
        self.row = row
        self.column = column
        self.distance = distance
        self.stepCost = stepCost
        self.position = (row, column)
        self.previous = previous
        self.isVisited = isVisited
        self.canVisit = canVisit

    def copy(self):
        return Cell(
            row=self.row,
            column=self.column,
            stepCost=self.stepCost,
            distance=self.distance,
            previous=self.previous,
            isVisited=self.isVisited,
            canVisit=self.canVisit
        )
    
    def __lt__(self, other):
        return self.distance < other.distance

class Field:
    _field=[[]]

    def __init__(self, _field=[[]]):
        self._field = [[Cell(i, j, cell, canVisit=cell != 0) for j, cell in enumerate(row)] for i, row in enumerate(_field)]
        
    def position_in_bound(self, row, column):
        return row >= 0 and row < len(self._field) and column >= 0 and column < len(self._field[0])

    def get_cell(self, row, column):
        return self._field[row][column]
    
    def set_value(self, row, column, value):
        self._field[row, column].value = value
    
    def copy(self):
        field_copy = Field()
        field = self._field
        field_copy._field = [[cell.copy() for cell in row] for row in field]
        return field_copy

class Pathfinder:
    def __init__(self, _field):
        self._field = Field(_field)

    directions = [(0,1),(1,0),(0,-1), (-1,0)]
              #, (1,1),(-1,-1), (1, -1), (-1, 1)]

    def dijkstra_pathfind(self, field, start_position, end_position):
        #field = self._field.copy()
        history = []
        start_row, start_column = start_position
        end_row, end_column = end_position
        if not field.position_in_bound(start_row, start_column) or not field.get_cell(start_row, start_column).canVisit or not field.get_cell(end_row, end_column).canVisit:
            return (None, None)
        p_queue = PriorityQueue()
        start_cell = field.get_cell(start_row, start_column)
        start_cell.distance = 0
        p_queue.put((start_cell.distance, start_cell))

        while not p_queue.empty():
            cell = p_queue.get()[1]

            if cell.isVisited:
                continue

            cell.isVisited = True
            history.append(cell.position)

            if cell.position == end_position:
                break

            row, column = cell.position
            for direction in self.directions:
                neighbour_row, neighbour_column = (row + direction[0], column + direction[1])
                
                if not field.position_in_bound(neighbour_row, neighbour_column):
                    continue

                neighbour_cell = field.get_cell(neighbour_row, neighbour_column)

                if not neighbour_cell.canVisit or neighbour_cell.isVisited:
                    continue
                
                nextDistance = cell.distance + neighbour_cell.stepCost

                if nextDistance < neighbour_cell.distance:
                    neighbour_cell.distance = nextDistance
                    neighbour_cell.previous = cell
                    p_queue.put((neighbour_cell.distance, neighbour_cell))
                    
        return (field,history)


    def choose_method(self, start_position, end_position, method):
        methods = {
            'dijkstra': self.dijkstra_pathfind,
            'bfs': self.bfs
        }

        if method not in methods:
            raise ValueError(f"Unknown method: {method}")

        return methods[method](self._field.copy(), start_position, end_position)


    def get_path(self, start_position, end_position, method = 'dijkstra'):
        _field, history = self.choose_method(start_position, end_position, method)
        path = []
        
        if not _field:
            return [], []
        
        end_cell = _field.get_cell(end_position[0], end_position[1])

        if not end_cell or not end_cell.isVisited:
            return (path,history)

        while end_cell != None:
            path.append((end_cell.row, end_cell.column))
            end_cell = end_cell.previous
        path.reverse()
        return (path, history)

    def bfs(self, field, start_position, end_position):
        #field = self._field.copy()
        history = []
        start_row, start_column = start_position
        end_row, end_column = end_position

        if not field.position_in_bound(start_row, start_column) or not field.get_cell(start_row, start_column).canVisit or not field.get_cell(end_row, end_column).canVisit:
            return (None, None)

        queue = deque([(start_row, start_column)])
        start_cell = field.get_cell(start_row, start_column)
        start_cell.isVisited = True
        start_cell.distance = 0

        while queue:
            current_row, current_column = queue.popleft()
            current_cell = field.get_cell(current_row, current_column)

            if (current_row, current_column) == end_position:
                break

            for direction in self.directions:
                new_row, new_column = current_row + direction[0], current_column + direction[1]

                if not field.position_in_bound(new_row, new_column):
                    continue

                neighbor_cell = field.get_cell(new_row, new_column)

                if neighbor_cell.canVisit and not neighbor_cell.isVisited:
                    neighbor_cell.isVisited = True
                    neighbor_cell.distance = current_cell.distance + 1
                    neighbor_cell.previous = current_cell
                    history.append((new_row, new_column))
                    queue.append((new_row, new_column))

        return (field, history)
     
