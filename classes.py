# -*- coding: utf-8 -*-
"""
classes module:

    Holds abstractions for all classes needed to derive solution

    Notes:  please view readme.md for design assumptions
"""

import utilities as utils


class Airport:
    """
    Defines a Airport instance

    Args:
        input_data_path(str): path to config text file, default is redwood.txt in project

    """

    def __init__(self, input_data_path):
        self.input_data = input_data_path
        self.roads = []
        self.intersections = []
        self.start = None
        self.destination = None
        self.parse_input_data()
        self._route_handler = RouteHandler(self)

    @property
    def route_handler(self):
        """
        Return the route_handler used in the class
        """
        return self._route_handler

    def parse_input_data(self):
        """
        Utility function that parses a given text file for airport definitions
        as defined in the problem statement
        """
        lines = [line.rstrip('\n') for line in open(self.input_data)]
        line_index = 0

        # Get Roads
        number_of_roads = lines[line_index]
        line_index += 1
        for n in range(0, int(number_of_roads)):
            road_tuple = tuple(lines[line_index].split(' '))
            self.roads.append(Road(road_tuple[0], road_tuple[1]))
            line_index += 1

        # Get intersections
        line_index += 1
        number_of_intersections = lines[line_index]
        line_index += 1
        for n in range(0, int(number_of_intersections)):
            intersection_tuple = tuple(lines[line_index].split(' '))
            self.intersections.append(Intersection(intersection_tuple[0], intersection_tuple[1], intersection_tuple[2],intersection_tuple[3]))
            line_index += 1

        # Set intersections for each road
        for road in self.roads:
            for intersection in self.intersections:
                if intersection.road_1 is road.name:
                    road.intersections.append(intersection)

        #  Set start and final destination
        line_index += 1
        self.start = tuple(lines[line_index].split(' '))
        line_index += 1
        self.destination = tuple(lines[line_index].split(' '))


class Road:
    """
    Defines a Road instance

    Args:
        name(str): name of the road
        radius(int): radius of the road

    """

    def __init__(self, name, radius):
        self._name = name
        self._radius = radius
        self._intersections = []

    @property
    def name(self):
        """
        Return the name used in the class
        """
        return self._name

    @property
    def radius(self):
        """
        Return the radius used in the class
        """
        return self._radius

    @property
    def intersections(self):
        """
        Return the intersections used in the class
        """
        return self._intersections


class Intersection:
    """
    Defines a Intersection instance

    Args:
        road_1(str): name of the first road
        point_1(int): degree of the first road
        road_2(str): name of the second road
        point_2(int): degree of the second road

    """
    def __init__(self, road_1, point_1, road_2, point_2):
        self._road_1 = road_1
        self._point_1 = point_1
        self._road_2 = road_2
        self._point_2 = point_2

    @property
    def road_1(self):
        """
        Return the road_1 used in the class
        """
        return self._road_1

    @property
    def point_1(self):
        """
        Return the point_1 used in the class
        """
        return self._point_1

    @property
    def road_2(self):
        """
        Return the road_2 used in the class
        """
        return self._road_2

    @property
    def point_2(self):
        """
        Return the point_2 used in the class
        """
        return self._point_2


class RouteHandler:
    """
    Class for handling class input abstractions and running algorithms to determined
    the shortest path/time for problem statement

    Args:
        airport(str): airport for handling
    """

    def __init__(self, airport):
        self._airport = airport
        self._road_path = [self._airport.start[0]]
        self._commands = []
        self._total_time = 0
        self._graph = Graph(self._airport)

    @property
    def airport(self):
        """
        Return the airport used in the class
        """
        return self._airport

    @property
    def road_path(self):
        """
        Return the road_path used in the class
        """
        return self._road_path

    @property
    def commands(self):
        """
        Return the commands used in the class
        """
        return self._commands

    @property
    def total_time(self):
        """
        Return the total used in the class
        """
        return self._total_time

    @property
    def graph(self):
        """
        Return the graph used in the class
        """
        return self._graph

    def get_shortest(self):
        """
        Delegation Function that runs private methods to get result of the problem statement
        """
        self.graph.run_dijkstra(self.graph.graph, self.graph.start_id, self.graph.destination_id)
        self._map_shortest_path_to_roads()
        self._translate_road_path_to_commands()
        utils.display_output(self.total_time, self.commands)

    def _map_shortest_path_to_roads(self):
        """
        Sets self.road_path by translating the node ids to the road transfers needed for each hop

        note bug in this code,  possible edge case where next and next_next node has two
        of the same way points so you wont be able tell which road to transfer too

        here would be a good application for a greedy algorithm
        """
        index = 0
        current_road = self.airport.start[0]
        for waypoint in self.graph.shortest_path:
            next_index = index + 1
            next_next_index = next_index + 1
            if next_next_index >= len(self.graph.shortest_path):
                # we already are on the final road
                return

            next_waypoint = self.graph.shortest_path[next_index]
            next_next_waypoint = self.graph.shortest_path[next_next_index]

            for node in self.graph.nodes:
                if node.id == next_waypoint:
                    next_node_points = node.points.copy()
                if node.id == next_next_waypoint:
                    next_next_node_points = node.points
            next_node_points.pop(current_road)

            temp_list = []
            for point in next_node_points:
                if next_next_node_points.get(point):
                    temp_list.append(point)

            # here is the bug,  possible that two points could be added here,
            # thus still ambiguous on which road to transfer too,  but the circle
            # would have to be on a different degree other then 180/0 or they would
            # be duplicate circles could add another follow up function that checks
            # proper distance if this were to happen, I attempted to design this in
            # a way that could handle as many edges cases from a intersection persective

            if len(temp_list) == 1:
                self.road_path.append(temp_list[0])
            index += 1

    def _translate_road_path_to_commands(self):
        """
        Sets self.commands with a list of commands needed to traverse the airport
        """
        index = 0
        stopped = True
        for current_waypoint in self.graph.shortest_path:
            next_index = index + 1
            if next_index == len(self.graph.shortest_path):
                # final waypoint return
                return
            next_waypoint = self.graph.shortest_path[next_index]

            # Check to see we need to change the orientation for the first waypoint
            if current_waypoint == self.graph.start_id:
                for node in self.graph.nodes:
                    if node.id == next_waypoint:
                        next_node_degree = node.points.get(self.airport.start[0])

                is_clockwise = utils.next_waypoint_is_clockwise(self.airport.start[1], next_node_degree)
                if self.airport.start[2] == '+' and not is_clockwise:
                    self.commands.append(('REVERSE', .03))
                    self.total_time += .03
                elif self.airport.start[2] == '-' and is_clockwise:
                    self.commands.append(('REVERSE', .03))
                    self.total_time += .03

            current_dis = self.graph.graph[current_waypoint][next_waypoint]
            seconds_to_next_waypoint = self._get_seconds_to_next(current_dis, stopped)
            # add travel to next waypoint
            self.commands.append(('GO', seconds_to_next_waypoint))
            self.total_time += seconds_to_next_waypoint
            # issue transfer command
            if index + 1 < len(self.road_path):
                self.commands.append(("TRANSFER {}".format(self.road_path[index + 1]), .01))
                self.total_time += .01
            index += 1

    def _get_seconds_to_next(self, distance, stopped):
        """
        Calculate seconds required to travel to next waypoint

        :param distance: distance in meters to next way point
        :type distance: int
        :param stopped: if the drone is currently at rest
        :type stopped: bool
        :rtype: int

        approach for if stopped:
        1 sec : speed : 1 : dis Covered : 1
        2 sec : speed : 2 : dis Covered : 3
        3 sec : speed : 3 : dis Covered : 6
        4 sec : speed : 4 : dis Covered : 10
                                  total : 34 m
        """
        total_seconds = 0
        if stopped:
            # handle all cases
            if distance == 1:
                return 1
            elif distance <= 3:
                return 2
            elif distance <= 6:
                return 3
            elif distance <= 10:
                return 4
            else:
                # account for start up acceleration cost and distance
                distance = distance - 34
                total_seconds = 4

        max_speed_intervals = distance / 4
        total_seconds += max_speed_intervals
        return round(total_seconds, 2)


class Graph:
    """
    Class for holding the directed graph data structure

    Args:
        airport(str): airport for handling
    """

    def __init__(self, airport):
        self.airport = airport
        self.graph = {}
        self.nodes = set()
        self.start_id = None
        self.destination_id = None
        self.shortest_path = None
        self._build_graph_nodes()
        self._build_graph_connections()

    def _build_graph_nodes(self):
        """
        Utility function that builds a dictionary of nodes for dijkstra's algorithm
        processing
        """
        node_count = 0
        # Filter all intersections into graph nodes and remove duplicate locations
        for intersection in self.airport.intersections:
             exists, node = self._node_exists(intersection)
             if exists:
                 self._update_node_points(node, intersection)
             else:
                 node_count += 1
                 new_node = GraphNode(node_count, intersection)
                 self.nodes.add(new_node)

        # set starting and final node ids if they already exist, if not create a new node
        for node in self.nodes:
            if node.points.get(self.airport.start[0]) == self.airport.start[1]:
                self.start_id = node.id
            if node.points.get(self.airport.destination[0]) == self.airport.destination[1]:
                self.destination_id = node.id

        if not self.start_id:
             node_count += 1
             new_node = GraphNode(node_count)
             new_node.points[self.airport.start[0]] = self.airport.start[1]
             self.nodes.add(new_node)
             self.start_id = new_node.id

        if not self.destination_id:
             node_count += 1
             new_node = GraphNode(node_count)
             new_node.points[self.airport.destination[0]] = self.airport.destination[1]
             self.nodes.add(new_node)

    def _node_exists(self, intersection):
        """
        Determind if this node already exists in our data sets
        :param intersection: intersection to checl
        :rtype: bool
        """
        # Check if a point on a road already exists e.g. { A 0, B 180} == {B 180, A 0}
        for node in self.nodes:
            if node.points.get(intersection.road_1) == intersection.point_1 or \
                node.points.get(intersection.road_2) == intersection.point_2:
                return True, node

        # Did not match any current nodes or no nodes exist yet
        return False, None

    def _update_node_points(self, node, intersection):
        """
        Updates the given node.points with a new road degree in given intersection

        :param node: graph node that already exists
        :param intersection: intersection with a new road degree
        """
        i1 = node.points.get(intersection.road_1)
        if not i1:
            node.points[intersection.road_1] = intersection.point_1
        else:
            node.points[intersection.road_2] = intersection.point_2

    def _build_graph_connections(self):
        """
        Sets self.graph as a directed graph of way points
        """

        for node in self.nodes:
            connections = {}
            other_nodes = self.nodes.copy()
            other_nodes.remove(node)
            for other_node in other_nodes:
                for point in node.points:
                    if other_node.points.get(point):
                        connections[other_node.id] = utils.get_arc_len(self.airport, node, other_node, point)
            self.graph[node.id] = connections

    def run_dijkstra(self, graph, src, dest, visited=[], distances={}, predecessors={}):
        """
        Runs dijkstra's algorithm to find shortest path for given source and destination

        :param graph: directed graph
        :param src: starting waypoint
        :param dest: finishing waypoint
        """
        # a few sanity checks
        if src not in graph:
            raise TypeError('The root of the shortest path tree cannot be found')
        if dest not in graph:
            raise TypeError('The target of the shortest path cannot be found')
            # ending condition
        if src == dest:
            # We build the shortest path and display it
            path = []
            pred = dest
            while pred != None:
                path.append(pred)
                pred = predecessors.get(pred, None)
            self.shortest_path = list(reversed(path))
        else:
            # if it is the initial  run, initializes the cost
            if not visited:
                distances[src] = 0
            # visit the neighbors
            for neighbor in graph[src]:
                if neighbor not in visited:
                    new_distance = distances[src] + graph[src][neighbor]
                    if new_distance < distances.get(neighbor, float('inf')):
                        distances[neighbor] = new_distance
                        predecessors[neighbor] = src
            # mark as visited
            visited.append(src)
            # now that all neighbors have been visited: recurse
            # select the non visited node with lowest distance 'x'
            # run Dijskstra with src='x'
            unvisited = {}
            for k in graph:
                if k not in visited:
                    unvisited[k] = distances.get(k, float('inf'))
            x = min(unvisited, key=unvisited.get)
            self.run_dijkstra(graph, x, dest, visited, distances, predecessors)


class GraphNode:
    """
    Child Class for representing a node in the Graph class
    Args:
        id(int): id of the current node
        intersection(Intersection): if given update the node points with the intersections degrees
    """

    def __init__(self, id, intersection=None):
        self._points = {}
        self._id = id
        if intersection:
            self.points[intersection.road_1] = intersection.point_1
            self.points[intersection.road_2] = intersection.point_2

    @property
    def points(self):
        """
        Return the points used in the class
        """
        return self._points

    @property
    def id(self):
        """
        Return the id used in the class
        """
        return self._id
