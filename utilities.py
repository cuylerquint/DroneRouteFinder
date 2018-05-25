# -*- coding: utf-8 -*-
"""
Utility module

    Functions that provide a small task for the classes module

"""
import math


def next_waypoint_is_clockwise(start_degree, next_node_degree):
    """
    Detereminds if the next waypoint is clockwise from the current waypoint

    :param start_degree: degree of current waypoint
    :param next_node_degree: degree of next waypoint
    :return:
    """
    result_degree = int(start_degree) + 180
    if result_degree > 360:
        result_degree -= 360
        if int(next_node_degree) <= int(result_degree):
            is_clockwise = True
        else:
            is_clockwise = False
    else:
        if int(next_node_degree) >= int(result_degree):
            is_clockwise = True
        else:
            is_clockwise = False

    return is_clockwise


def get_arc_len(airport, root_node, child_node, road_key):
    """
    Calculates the arc lenght between two way points for a given road

    :param airport: airport instance for current promblem
    :param root_node: current waypoint
    :param child_node: next waypoint
    :param road_key: road that were currenlt working on
    :return: rounded arc length
    """
    arc_length = None
    for road in airport.roads:
        if road.name == road_key:
            angle = get_angle(root_node.points.get(road_key), child_node.points.get(road_key))
            arc_length = angle * float(road.radius)

    return round(arc_length, 3)


def get_angle(root_angle, child_angle):
    """
    Given two degrees of a cicrle calculate the theta of them

    :param root_angle: degree of current waypoint
    :param child_angle: degree of next waypoint
    :return: theta angle
    """
    root_node_radians = math.radians(float(root_angle))
    child_node_radians = math.radians(float(child_angle))

    x1 = math.cos(root_node_radians)
    y1 = math.sin(root_node_radians)
    x2 = math.cos(child_node_radians)
    y2 = math.sin(child_node_radians)

    dot_product = x1 * x2 + y1 * y2
    return math.acos(dot_product)


def display_output(total_time, commands):
    """
    Displays the programs output as defined in problem statement

    :param total_time: total elasped time to travesre airport from start to finish
    :param commands: commands needed to traverse airport
    """
    print round(total_time, 1)
    for command in commands:
        print "{} ({})".format(command[0], command[1])
