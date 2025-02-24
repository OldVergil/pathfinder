from collections import deque
from queue import PriorityQueue
from lee_algorithm import Field

directions = [(0,1),(1,0),(0,-1), (-1,0)]
              #, (1,1),(-1,-1), (1, -1), (-1, 1)]

def heuristic(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

def dijkstra_pathfind(matrix, start_position, end_position):
    field = Field(matrix)
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
        for direction in directions:
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
            

def get_path(matrix, start_position, end_position, method = 'dijkstra'):
    if method == 'bfs':
        field, history = bfs(matrix, start_position, end_position)
    elif method == 'dijkstra':
        field, history = dijkstra_pathfind(matrix, start_position, end_position)
    path = []
    
    if not field:
        return [], []
    
    end_cell = field.get_cell(end_position[0], end_position[1])

    if not end_cell or not end_cell.isVisited:
        return (path,history)

    while end_cell != None:
        path.append((end_cell.row, end_cell.column))
        end_cell = end_cell.previous
    path.reverse()
    return (path, history)


def bfs(matrix, start_position, end_position):
    """
    Алгоритм BFS для поиска кратчайшего пути.
    """
    field = Field(matrix)
    history = []
    start_row, start_column = start_position
    end_row, end_column = end_position

    # Проверка, что начальная позиция допустима
    if not field.position_in_bound(start_row, start_column) or not field.get_cell(start_row, start_column).canVisit or not field.get_cell(end_row, end_column).canVisit:
        return (None, None)

    # Инициализация очереди и отметка начальной позиции как посещенной
    queue = deque([(start_row, start_column)])
    start_cell = field.get_cell(start_row, start_column)
    start_cell.isVisited = True
    start_cell.distance = 0

    while queue:
        current_row, current_column = queue.popleft()
        current_cell = field.get_cell(current_row, current_column)

        if (current_row, current_column) == end_position:
            break

        # Перебор всех направлений
        for direction in directions:
            new_row, new_column = current_row + direction[0], current_column + direction[1]

            # Проверка, что новая позиция допустима
            if not field.position_in_bound(new_row, new_column):
                continue

            neighbor_cell = field.get_cell(new_row, new_column)

            # Если клетка доступна и не посещена
            if neighbor_cell.canVisit and not neighbor_cell.isVisited:
                neighbor_cell.isVisited = True
                neighbor_cell.distance = current_cell.distance + 1
                neighbor_cell.previous = current_cell
                history.append((new_row, new_column))
                queue.append((new_row, new_column))

    return (field, history)


