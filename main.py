# -*- coding: utf-8 -*-
"""
main module:
  entry point for Tests module

  starting point for progarm,  fetchs input data path from user
  then inits a airport class for processing the problem statement

"""
from classes import *
import sys


def main():
    if len(sys.argv) < 2:
        print "Please pass a .txt file as the second argument to this progarm"
        sys.exit()
    input_data_path = sys.argv[1]
    airport = Airport(input_data_path)
    airport.route_handler.get_shortest()


if __name__ == '__main__':
    main()