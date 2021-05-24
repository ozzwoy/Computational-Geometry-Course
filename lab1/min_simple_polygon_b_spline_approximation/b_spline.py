import graphics
import numpy as np


class QuadraticBSpline:
    num_of_segments = 50

    # A * t^2 + B * t + C, t є [2, 3]
    def __init__(self, point_a, point_b, point_c):
        self.A = point_a
        self.B = point_b
        self.C = point_c
        self.lines = []

    def __value_at(self, t):
        return self.A * t ** 2 + self.B * t + self.C

    def __build_lines(self):
        n = QuadraticBSpline.num_of_segments
        self.lines.clear()
        nodes = [x / n for x in range(n + 1)]

        for i in range(len(nodes) - 1):
            current_point = self.__value_at(nodes[i])
            next_point = self.__value_at(nodes[i + 1])
            self.lines.append(graphics.Line(graphics.Point(current_point[0], current_point[1]),
                                            graphics.Point(next_point[0], next_point[1])))
            self.lines[-1].setWidth(2)

    def draw(self, window, color):
        self.__build_lines()
        for line in self.lines:
            line.setFill(color)
            line.setOutline(color)
            line.draw(window)

    def undraw(self):
        for line in self.lines:
            line.undraw()


class BSplineApproximation:
    matrix = np.array([[1, -2, 1],
                       [-2, 2, 1],
                       [1, 0, 0]])

    @staticmethod
    def approximate(points):
        matrix = BSplineApproximation.matrix
        splines = []

        for i in range(len(points)):
            cur_points = np.array([np.array([points[i].x, points[i].y]),
                                   np.array([points[(i + 1) % len(points)].x, points[(i + 1) % len(points)].y]),
                                   np.array([points[(i + 2) % len(points)].x, points[(i + 2) % len(points)].y])])
            cur_points = cur_points.transpose()
            result = 0.5 * cur_points.dot(matrix).transpose()
            splines.append(QuadraticBSpline(result[0], result[1], result[2]))

        return splines
