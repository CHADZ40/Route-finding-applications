"""Tests for Member 5 - Road blocking and traffic simulation."""

import unittest

import sys
from pathlib import Path

# Lets you run this file directly (e.g. the Run button in VS Code).
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from study_case.member1_graph import load_sample_graph
from study_case.member2_dijkstra import PathResult, dijkstra
from study_case.member3_astar import astar
from study_case.member5_road_blocking import (apply_traffic, blocked_roads, compare_routes,
                                              find_route_avoiding)
from test_case.test_member2_dijkstra import make_graph


class TestRoadBlocking(unittest.TestCase):
    def test_roads_restored_after_block(self):
        graph = make_graph()
        with blocked_roads(graph, [("A", "B")]):
            self.assertFalse(graph.has_road("A", "B"))
        self.assertTrue(graph.has_road("A", "B"))
        self.assertEqual(graph.get_weight("B", "A"), 1.0)

    def test_roads_restored_after_error(self):
        graph = make_graph()
        with self.assertRaises(RuntimeError):
            with blocked_roads(graph, [("A", "B")]):
                raise RuntimeError("boom")
        self.assertTrue(graph.has_road("A", "B"))

    def test_blocking_missing_road_restores_earlier_ones(self):
        graph = make_graph()
        with self.assertRaises(KeyError):
            with blocked_roads(graph, [("A", "B"), ("A", "E")]):
                pass
        self.assertTrue(graph.has_road("A", "B"))

    def test_find_route_avoiding(self):
        graph = make_graph()
        result = find_route_avoiding(graph, "A", "C", [("B", "C")])
        self.assertEqual(result.path, ["A", "D", "C"])
        self.assertAlmostEqual(result.distance, 4.0)

    def test_find_route_avoiding_with_astar(self):
        result = find_route_avoiding(load_sample_graph(), "Home", "Airport",
                                     [("Library", "Hospital")], algorithm=astar)
        self.assertNotIn(("Library", "Hospital"), list(zip(result.path, result.path[1:])))
        self.assertAlmostEqual(result.distance, 13.3)

    def test_all_routes_blocked(self):
        result = find_route_avoiding(make_graph(), "A", "C", [("A", "B"), ("A", "C"), ("A", "D")])
        self.assertFalse(result.found)


class TestTraffic(unittest.TestCase):
    def test_traffic_changes_route_without_touching_original(self):
        graph = make_graph()
        slowed = apply_traffic(graph, {("A", "B"): 5})
        self.assertEqual(dijkstra(slowed, "A", "C").path, ["A", "D", "C"])
        self.assertEqual(graph.get_weight("A", "B"), 1.0)

    def test_invalid_factor(self):
        with self.assertRaises(ValueError):
            apply_traffic(make_graph(), {("A", "B"): 0.5})

    def test_compare_routes(self):
        summary = compare_routes(PathResult(["A"], 10.0), PathResult(["A"], 12.0))
        self.assertAlmostEqual(summary["extra"], 2.0)
        self.assertAlmostEqual(summary["percent"], 20.0)


if __name__ == "__main__":
    unittest.main()
