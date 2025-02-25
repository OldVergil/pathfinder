from collections import deque
from queue import PriorityQueue
from field import Field

class Pathfinder:
    directions = [(0,1),(1,0),(0,-1), (-1,0)] 
    #[(1,1),(-1,-1), (1, -1), (-1, 1)]

    def check_positions_in_bound(self, field, start_position, end_position):
        start_row, start_column = start_position
        end_row, end_column = end_position
        return field.position_in_bound(start_row, start_column) and field.position_in_bound( end_row, end_column)
        
    def check_cells_can_visited(self, field, start_position, end_position):
        start_row, start_column = start_position
        end_row, end_column = end_position
        start_cell = field.get_cell(start_row, start_column)
        end_cell = field.get_cell(end_row, end_column)
        return start_cell.canVisit and end_cell.canVisit
    
    def check(self, field, start_position, end_position):
        return self.check_positions_in_bound(field, start_position, end_position) and self.check_cells_can_visited(field, start_position, end_position)

    def dijkstra_pathfind(self, field, start_position, end_position):
        history = []
        start_row, start_column = start_position
        
        if not self.check(field, start_position, end_position):
            return (None, None)
        
        start_cell = field.get_cell(start_row, start_column)

        p_queue = PriorityQueue()
        start_cell.distance = 0
        p_queue.put((start_cell.distance, start_cell))

        while not p_queue.empty():
            cell = p_queue.get()[1]

            if cell.isVisited:
                continue

            cell.isVisited = True
            history.append(cell)

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

    def bfs(self, field, start_position, end_position):
        start_row, start_column = start_position

        if not self.check(field, start_position, end_position):
            return (None, None)  

        start_cell = field.get_cell(start_row, start_column)
        queue = deque([(start_row, start_column)])
        start_cell.isVisited = True
        start_cell.distance = 0
        history = [start_cell]

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
                    history.append(neighbor_cell)
                    queue.append((new_row, new_column))

        return (field, history)

    def choose_method(self, field, start_position, end_position, method):
        methods = {
            'dijkstra': self.dijkstra_pathfind,
            'bfs': self.bfs
        }

        if method not in methods:
            raise ValueError(f"Unknown method: {method}")

        return methods[method](field.copy(), start_position, end_position)

    def get_path(self, field, start_position, end_position, method = 'dijkstra'):
        field, history = self.choose_method(field, start_position, end_position, method)
        path = []
        
        if not field:
            return ([], [])
        
        end_cell = field.get_cell(end_position[0], end_position[1])

        if not end_cell.isVisited:
            return ([], history)

        while end_cell != None:
            path.append(end_cell)
            end_cell = end_cell.previous
        path.reverse()
        return (path, history)

    
     
