"""Tests for Menghour - Dijkstra's algorithm."""

import math
import unittest

from study_case.member1_graph import Graph, load_sample_graph
from study_case.member2_dijkstra import dijkstra, reconstruct_path, shortest_distances


def make_graph() -> Graph:
    """A-B-C is shorter (2) than the direct road A-C (5). E is unreachable."""
    graph = Graph()
    for name, x, y in [("A", 0, 0), ("B", 1, 0), ("C", 2, 0), ("D", 1, 1), ("E", 5, 5)]:
        graph.add_location(name, x, y)
    graph.add_road("A", "B", 1)
    graph.add_road("B", "C", 1)
    graph.add_road("A", "C", 5)
    graph.add_road("A", "D", 2)
    graph.add_road("D", "C", 2)
    return graph


class TestDijkstra(unittest.TestCase):
    def test_finds_shortest_path(self):
        result = dijkstra(make_graph(), "A", "C")
        self.assertEqual(result.path, ["A", "B", "C"])
        self.assertAlmostEqual(result.distance, 2.0)
        self.assertTrue(result.found)
        self.assertEqual(result.algorithm, "Dijkstra")

    def test_start_equals_goal(self):
        result = dijkstra(make_graph(), "A", "A")
        self.assertEqual(result.path, ["A"])
        self.assertEqual(result.distance, 0.0)

    def test_unreachable(self):
        result = dijkstra(make_graph(), "A", "E")
        self.assertFalse(result.found)
        self.assertEqual(result.distance, math.inf)

    def test_unknown_location(self):
        with self.assertRaises(KeyError):
            dijkstra(make_graph(), "A", "Z")

    def test_shortest_distances(self):
        dist = shortest_distances(make_graph(), "A")
        self.assertEqual(dist, {"A": 0.0, "B": 1.0, "C": 2.0, "D": 2.0, "E": math.inf})

    def test_reconstruct_path(self):
        self.assertEqual(reconstruct_path({"B": "A", "C": "B"}, "A", "C"), ["A", "B", "C"])
        self.assertEqual(reconstruct_path({}, "A", "C"), [])

    def test_sample_map_route(self):
        result = dijkstra(load_sample_graph(), "Home", "Airport")
        self.assertEqual(result.path, ["Home", "School", "Library", "Hospital", "Airport"])
        self.assertAlmostEqual(result.distance, 13.1)

    def test_matches_shortest_distances_on_sample_map(self):
        graph = load_sample_graph()
        dist = shortest_distances(graph, "Home")
        for goal in graph.locations:
            self.assertAlmostEqual(dijkstra(graph, "Home", goal).distance, dist[goal])


if __name__ == "__main__":
    unittest.main()
