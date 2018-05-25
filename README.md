# Airport Drone Route Finder

This code base is a solution to the task defined in *DroneRouteFinderChallenge.txt*.
Before continuing please review the *DroneRouteFinderChallenge.txt* to understand
the problem statement.

## Assumptions
- Not all intersections will be at 0 or 180 degree's did not want to ad-hoc a solution

- All circle degrees are from 0 to the left and 180 to the right for orientation calculations

- Drone does not have to be stop to do a transfer

- Drone starts stopped

- Drone travels only on the road edges/circumferences, inferred this because of orientation is on clockwise/counter clockwise
  design of solution is based completely on this as distances are derived from arc lengths

## Design

- This solution can be divided into three major steps:
   1) Translation of input data into a airport instance with road/intersection definitions
   2) A directed graph data structure is formed to represent this airport
   3) Dijkstra's algorithm is ran on the graph to get the shortest path and then outputted

- Graph Notes
  * I did not want to complicate the graph structure by having node for each intersection,
    so i removed duplicate of where different road intersections shared the same way point
  * The expected graph going into the Dijkstra function looks like this : { 1 : { 2 : dis_in_meters, 3 : dis}, 2 : { 1 : dis, 4 : dis}, ... }


## Running

- python tests.py || python main.py $path_to_input_data.txt

- note to run tests.py you will need the ddt package installed : https://github.com/datadriventests/ddt

## Improvements

- Use a greedy algorithm to find next road in translation from waypoint shortest_path to road_path to
    fix bug outlined in source code  see function classes._map_shortest_path_to_roads

- Better Usage/implementation of commands,  currently relies on heavy assumptions, edge cases where
    reserve would be needed

- More unit tests!

## Author
- **Cuyler Quint** - [cuylerquint](https://github.com/cuylerquint)
