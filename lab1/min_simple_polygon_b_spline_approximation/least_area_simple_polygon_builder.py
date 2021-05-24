from jarvis_march import JarvisMarch
import utils


class LeastAreaSimplePolygonBuilder:

    @staticmethod
    def build(points):
        hull = JarvisMarch.execute(points)
        residual_points = [p for p in points if p not in hull.points]

        while len(residual_points) != 0:
            max_area = 0
            vertex_index = -1
            point_index = -1

            for i in range(len(hull.points)):
                cur_index = i
                next_index = (i + 1) % len(hull.points)
                cur_vertex = hull.points[cur_index]
                next_vertex = hull.points[next_index]

                for j in range(len(residual_points)):
                    correct = True

                    for p in residual_points:
                        if p != residual_points[j]:
                            if utils.belongs_to_triangle(cur_vertex, next_vertex, residual_points[j], p):
                                correct = False
                                break
                    if not correct:
                        continue

                    for k in range(len(hull.points)):
                        if k != cur_index:
                            e1 = hull.points[k]
                            e2 = hull.points[(k + 1) % len(hull.points)]

                            x, y = utils.intersect_segments(e1, e2, cur_vertex, residual_points[j])
                            if x is not None and not (e2 == cur_vertex and x == cur_vertex.x and y == cur_vertex.y):
                                correct = False
                                break

                            x, y = utils.intersect_segments(e1, e2, next_vertex, residual_points[j])
                            if x is not None and not (e1 == next_vertex and x == next_vertex.x and y == next_vertex.y):
                                correct = False
                                break
                    if not correct:
                        continue

                    area = utils.triangle_area(cur_vertex, next_vertex, residual_points[j])
                    if area > max_area:
                        max_area = area
                        vertex_index = next_index
                        point_index = j

            hull.points.insert(vertex_index, residual_points[point_index])
            residual_points.pop(point_index)

        return hull
