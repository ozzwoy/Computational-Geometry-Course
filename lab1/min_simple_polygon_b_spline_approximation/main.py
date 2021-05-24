from enum import Enum
import graphics
from b_spline import BSplineApproximation
from entities import Point
from least_area_simple_polygon_builder import LeastAreaSimplePolygonBuilder
import random


def generate_points(n):
    points = []
    for i in range(n):
        points.append(Point(random.randint(0, Main.width), random.randint(0, Main.height)))
    return points


class Main:
    class Mode(Enum):
        INTERACTIVE = 0
        RANDOM = 1

    mode = Mode.INTERACTIVE
    width = 1000
    height = 700
    win = graphics.GraphWin("Least area simple polygon approximation", width, height)
    points = []
    hull = None
    splines = None

    @staticmethod
    def on_mouse_click(event):
        point = Point(event.x, event.y)
        if any(point.x == p.x and point.y == p.y for p in Main.points):
            return
        Main.points.append(point)
        point.draw(Main.win)

        if len(Main.points) > 2:
            if Main.hull is not None:
                Main.hull.undraw(Main.win)
            Main.hull = LeastAreaSimplePolygonBuilder.build(Main.points)
            Main.hull.draw(Main.win, "red")

            if Main.splines is not None:
                for spline in Main.splines:
                    spline.undraw()
            Main.splines = BSplineApproximation.approximate(Main.hull.points)
            for spline in Main.splines:
                spline.draw(Main.win, "green")

    @staticmethod
    def main():
        if Main.mode == Main.Mode.INTERACTIVE:
            Main.win.setMouseHandler(Main.on_mouse_click)
        else:
            points = generate_points(30)
            hull = LeastAreaSimplePolygonBuilder.build(points)
            hull.draw(Main.win, "red")
            splines = BSplineApproximation.approximate(hull.points)
            for spline in splines:
                spline.draw(Main.win, "green")

        Main.win.mainloop()


if __name__ == '__main__':
    Main.main()
