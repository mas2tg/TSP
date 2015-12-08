from PIL import ImageStat
from queue import PriorityQueue
import random
import math


def get_density(image, x, y):
    """
    Return the density of a point
    :param image: The image being stippled
    :param x: x coordinate of the point
    :param y: y coordinate of the point
    :return: A number between 0 and 1, the density of the given point
    """
    density = 1 - image.getpixel((x, y))/255
    return density


def get_centroids(image, discrete_voronoi_diagram, list_of_generators):
    """
    Return a list of centroids as calculated by the list of generators and the voronoi diagram
    :param image: The image being stippled
    :param discrete_voronoi_diagram: the DVD
    :param list_of_generators: a list of generators that generated the DVD
    :return: A list of centroids
    """
    width, length = image.size
    mass = [0 for i in range(len(list_of_generators))]
    x_mass = [0 for i in range(len(list_of_generators))]
    y_mass = [0 for i in range(len(list_of_generators))]

    for y in range(length):
        for x in range(width):
            value = discrete_voronoi_diagram[y][x]
            mass[value] += get_density(image, x, y)
            x_mass[value] += x * get_density(image, x, y)
            y_mass[value] += y * get_density(image, x, y)

    list_of_centroids = [(0,0) for i in range(len(list_of_generators))]
    for i in range(len(list_of_centroids)):
        if mass[i] > 0:
            list_of_centroids[i] = (x_mass[i]/mass[i], y_mass[i]/mass[i])

    return list_of_centroids


def get_initial_generators(image):
    """
    Return a list of initial generating points using rejection sampling.
    :param image: The image being stippled
    :return: a list of initial generating points
    """
    width, length = image.size
    spacing = 2
    list_of_generators = []

    for i in range(0, width-int(spacing/2), spacing):
        for j in range(0, length-int(spacing/2), spacing):
            area = image.crop((i, j, i + spacing, j + spacing))
            if ImageStat.Stat(area).mean[0]/255 < random.random():
                list_of_generators.append((i + int(spacing/2), j + int(spacing/2)))
    print('Finished getting first generators')
    return list_of_generators


def get_initial_generators_2(image):
    width, length = image.size
    list_of_generators = []

    for i in range(0, width-1, 2):
        for j in range(0, length-1, 2):
            area = image.crop((i, j, i + 2, j + 2))
            if ImageStat.Stat(area).mean[0] > 127.5:
                list_of_generators.append((i + 1, j + 1))

    return list_of_generators


def get_discrete_voronoi_diagram(image, list_of_generators):
    """
    Given an image and a list of generating points, return the discrete voronoi diagram. The DVD is represented
    by a matrix of numbers, with each number being a different color(section) of the DVD
    :param image: The image being stippled
    :param list_of_generators: A list of generating points
    :return: The discrete voronoi diagram
    """
    width, length = image.size
    discrete_voronoi_diagram = [[-1 for x in range(width)] for y in range(length)]

    queue = PriorityQueue()
    for i in range(len(list_of_generators)):
        if 0 <= list_of_generators[i][0] <= width and 0 <= list_of_generators[i][1] <= length:
            queue.put((0, list_of_generators[i], i))

    while not queue.empty():
        triple = queue.get()
        point_coordinate = triple[1]
        x_coor = point_coordinate[0]
        y_coor = point_coordinate[1]
        i = triple[2]

        if discrete_voronoi_diagram[y_coor][x_coor] == -1:
            discrete_voronoi_diagram[y_coor][x_coor] = i

            neighboring_points = [(x_coor, y_coor+1), (x_coor+1, y_coor), (x_coor, y_coor-1), (x_coor-1, y_coor)]
            for item in neighboring_points:
                if 0 <= item[0] < width and 0 <= item[1] < length:
                    if discrete_voronoi_diagram[item[1]][item[0]] == -1:
                        distance = math.sqrt((item[0] - list_of_generators[i][0])**2 +
                                             (item[1] - list_of_generators[i][1])**2)
                        queue.put((distance, item, i))

    return discrete_voronoi_diagram


def stipple(image):
    """
    Return a set of points representing the stippling points
    :param image: The image being stippled
    :return: a set of points
    """
    list_of_generators = get_initial_generators(image)

    for i in range(3):
        dvd = get_discrete_voronoi_diagram(image, list_of_generators)
        centroids = get_centroids(image, dvd, list_of_generators)
        list_of_generators = [(round(pt[0]), round(pt[1])) for pt in centroids]
        print(i, 'iteration')

    return list_of_generators
