# -*- coding: utf-8 -*-
"""
Tests module:
  Defines Tests class and tests classes and utilities modules

"""

import ddt
import unittest
import os

import classes as classes
import utilities as utils


class ClassesTests(unittest.TestCase):

    def test_given_data_set(self):
        test_data_path = os.path.dirname(os.getcwd()) + '/DroneRouteFinder/test_data.txt'
        airport = classes.Airport(test_data_path)
        airport.route_handler.get_shortest()
        self.assertEqual(airport.route_handler.graph.shortest_path, [5, 1, 3])
        self.assertEqual(round(airport.route_handler.total_time, 1), 830.9)
        self.assertEqual(airport.route_handler.commands, [('GO', 50.04), ('TRANSFER B', 0.01), ('GO', 780.9)])


@ddt.ddt
class UtilitiesTests(unittest.TestCase):

    @ddt.data(
        (355, 0, True),
        (170, 0, False),
    )
    def test_next_waypoint_is_clockwise(self, args):
        start_degree, next_node_degree, is_clockwise = args
        result = utils.next_waypoint_is_clockwise(start_degree, next_node_degree)
        if is_clockwise:
            self.assertTrue(result)
        else:
            self.assertFalse(result)


if __name__ == '__main__':
    unittest.main()
