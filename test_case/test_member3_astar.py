"""Tests for Kheang - A* algorithm and performance comparison."""

import math
import unittest

import sys
from pathlib import Path

# Lets you run this file directly (e.g. the Run button in VS Code).
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from study_case.member1_graph import load_sample_graph
from study_case.member2_dijkstra import dijkstra
from study_case.member3_astar import (astar, compare_algorithms, euclidean_heuristic,
                                      generate_grid_graph, timed, zero_heuristic)
from test_case.test_member2_dijkstra import make_graph


class TestAStar(unittest.TestCase):
    def test_finds_shortest_path(self):
        result = astar(make_graph(), "A", "C")
        self.assertEqual(result.path, ["A", "B", "C"])
        self.assertAlmostEqual(result.distance, 2.0)
        self.assertEqual(result.algorithm, "A*")

    def test_unreachable(self):
        result = astar(make_graph(), "A", "E")
        self.assertFalse(result.found)
        self.assertEqual(result.distance, math.inf)

    def test_heuristic(self):
        graph = make_graph()
        self.assertAlmostEqual(euclidean_heuristic(graph, "A", "E"), math.hypot(5, 5))
        self.assertEqual(zero_heuristic(graph, "A", "E"), 0.0)

    def test_same_distance_as_dijkstra_on_sample_map(self):
        graph = load_sample_graph()
        for start in graph.locations:
            for goal in graph.locations:
                self.assertAlmostEqual(astar(graph, start, goal).distance,
                                       dijkstra(graph, start, goal).distance)

    def test_same_distance_as_dijkstra_on_grid(self):
        graph = generate_grid_graph(15, 15, seed=1)
        self.assertAlmostEqual(astar(graph, "0,0", "14,14").distance,
                               dijkstra(graph, "0,0", "14,14").distance)

    def test_astar_visits_fewer_locations_on_grid(self):
        graph = generate_grid_graph(30, 30, seed=7)
        self.assertLess(astar(graph, "0,0", "29,29").nodes_visited,
                        dijkstra(graph, "0,0", "29,29").nodes_visited)


class TestPerformance(unittest.TestCase):
    def test_timed_decorator(self):
        result, elapsed = timed(sum)([1, 2, 3])
        self.assertEqual(result, 6)
        self.assertGreaterEqual(elapsed, 0.0)

    def test_compare_algorithms(self):
        rows = compare_algorithms(load_sample_graph(), [("Home", "Airport")], repeats=2)
        self.assertEqual([r.algorithm for r in rows], ["Dijkstra", "A*"])
        self.assertAlmostEqual(rows[0].distance, rows[1].distance)

    def test_grid_generator(self):
        graph = generate_grid_graph(3, 4, seed=0)
        self.assertEqual(len(graph), 12)
        self.assertEqual(graph.road_count(), 3 * 3 + 2 * 4)


if __name__ == "__main__":
    unittest.main()
