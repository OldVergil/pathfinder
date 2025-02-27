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
        self.screenCoord = (column, row )

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