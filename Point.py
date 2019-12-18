class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __str__(self):
        if self.x == "O":
            return "Infinity point"
        return str(self.x) + "," + str(self.y)
