class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __str__(self):
        if self.x == "O":
            return "O"
        return str(self.x) + "," + str(self.y)
