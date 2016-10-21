from itertools import product, izip
import json
import random
import heapq
from PIL import Image
from math import sqrt

u = (3, 5)
v = (7, 15)

def mult(vec, scalar):
    return (vec[0] * scalar, vec[1] * scalar)

def add(vecA, vecB):
    return (vecA[0] + vecB[0], vecA[1] + vecB[1])

def subtract(vecA, vecB):
    return (vecA[0] - vecB[0], vecA[1] - vecB[1])

def magnitude(vec):
    return sqrt((vec[0] ** 2) + (vec[1] ** 2))

moves = [add(mult(u, m), mult(v, n)) for m, n in product([-1, 0, 1], [-1, 0, 1])]
max_move_distance = max(map(magnitude, moves))

curr_color = 0
colors = {} # point: color
neighbours = [] # (distance, point)  the closest point to the center, that is adjacent to a colored point
work = [] # (distance, point) colored, but not explored moves from here

def insert_uniq(l, x):
    if x in l:
        return
    heapq.heappush(l, x)

def outside_bounds(vec):
    return vec[0] < 0 or vec[1] < 0

def explore_moves(point):
    col = colors[point]
    for move in moves:
        new_point = add(point, move)
        if new_point in colors:
            continue
        if outside_bounds(new_point):
            continue # dont explore in every direction
        color(new_point, col)

def color(point, col):
    colors[point] = col
    insert_uniq(work, (magnitude(point), point))
    add_neighbours(point)

def add_neighbours(point):
    for neighbour in [add(point, (1, 0)), add(point, (0, 1))]:
        if neighbour in colors:
            continue
        insert_uniq(neighbours, (magnitude(neighbour), neighbour))

def complete():
    if len(colors) == 0:
        return False
    start = (0,0)
    start_color = colors[start]
    x_lim = (1,0)
    while True:
        if not x_lim in colors:
            return False
        if colors[x_lim] == start_color:
            break
        x_lim = add(x_lim, (1,0))

    y_lim = (0, 1)
    while True:
        if not y_lim in colors:
            return False
        if colors[y_lim] == start_color:
            break
        y_lim = add(y_lim, (0,1))
    x = x_lim[0]
    y = y_lim[1]
    for point in product(range(x), range(y)):
        if not point in colors:
            return False

    output = []

    for point_x in range(x):
        output.append([])
        for point_y in range(y):
            output[point_x].append(colors[(point_x, point_y)])

    for l in output:
        print l

    def random_color():
        r = random.randint(0, 255)
        g = random.randint(0, 255)
        b = random.randint(0, 255)
        return (r, g, b)

    color_map = [random_color() for i in range(curr_color+ 1)]

    img = Image.new('RGB', (100, 100))
    for pix_x in range(100):
        for pix_y in range(100):
            img.putpixel((pix_x, pix_y), color_map[colors[(pix_x % x, pix_y % y)]])
    img.show()


    return True

while not complete():
    distance = 0
    point = (0, 0)
    while point in colors:
        distance, point = heapq.heappop(neighbours)
    # if we cant possibly reach this point from the next point on the work queue, then introduce a new color
    if len(work) == 0 or distance < work[0][0] - max_move_distance:
        curr_color += 1
        color(point, curr_color)
        print curr_color
    else:
        heapq.heappush(neighbours, (distance, point))# put back on the neighbours queue, still more exploring to do
        distance, point = heapq.heappop(work)
        explore_moves(point)
