import math


def polar_angle(origin, point):
    x = point.x - origin.x
    y = point.y - origin.y

    if x > 0:
        if y >= 0:
            return math.atan(y / x)
        else:
            return 2 * math.pi + math.atan(y / x)
    elif x < 0:
        return math.pi + math.atan(y / x)
    else:
        if y > 0:
            return math.pi / 2
        elif y < 0:
            return 3 * math.pi / 2
        else:
            return None


# >0 if counterclockwise ("left turn"), =0 if collinear, <0 if clockwise ("right turn")
def ccw(p1, p2, p3):
    return (p2.x - p1.x) * (p3.y - p1.y) - (p2.y - p1.y) * (p3.x - p1.x)


def triangle_area(v1, v2, v3):
    return abs(v1.x * v2.y + v2.x * v3.y + v3.x * v1.y - v1.y * v2.x - v2.y * v3.x - v3.y * v1.x) / 2


def belongs_to_triangle(v1, v2, v3, point):
    d1 = ccw(point, v1, v2)
    d2 = ccw(point, v2, v3)
    d3 = ccw(point, v3, v1)

    has_neg = (d1 < 0) or (d2 < 0) or (d3 < 0)
    has_pos = (d1 > 0) or (d2 > 0) or (d3 > 0)

    return not (has_neg and has_pos)


def intersect_lines(p11, p12, p21, p22):
    a1 = p12.y - p11.y
    b1 = p11.x - p12.x
    c1 = a1 * p11.x + b1 * p11.y

    a2 = p22.y - p21.y
    b2 = p21.x - p22.x
    c2 = a2 * p21.x + b2 * p21.y

    det = a1 * b2 - a2 * b1
    if det == 0:
        # lines are parallel
        return None, None

    x = (b2 * c1 - b1 * c2) / det
    y = (a1 * c2 - a2 * c1) / det
    return x, y


def intersect_segments(p11, p12, p21, p22):
    x, y = intersect_lines(p11, p12, p21, p22)
    if x is None:
        return x, y

    if (p11.x < x < p12.x or p12.x < x < p11.x) and \
            (p21.x < x < p22.x or p22.x < x < p21.x) and \
            (p11.y < y < p12.y or p12.y < y < p11.y) and \
            (p21.y < y < p22.y or p22.y < y < p21.y):
        return x, y

    return None, None
