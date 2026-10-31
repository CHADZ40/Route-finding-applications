"""Tests for Member 1 - Graph class and data loading."""

import json
import tempfile
import unittest
import sys
from pathlib import Path

# Lets you run this file directly (e.g. the Run button in VS Code).
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from study_case.member1_graph import Graph, graph_from_dict, load_graph_from_json, load_sample_graph


def make_graph() -> Graph:
    graph = Graph()
    for name, x, y in [("A", 0, 0), ("B", 1, 0), ("C", 2, 0)]:
        graph.add_location(name, x, y)
    graph.add_road("A", "B", 1)
    graph.add_road("B", "C", 2)
    return graph


class TestGraph(unittest.TestCase):
    def test_add_location_and_road(self):
        graph = make_graph()
        self.assertEqual(len(graph), 3)
        self.assertEqual(graph.road_count(), 2)
        self.assertIn("A", graph)
        self.assertEqual(graph.location("B").x, 1.0)

    def test_undirected_roads_go_both_ways(self):
        graph = make_graph()
        self.assertEqual(graph.get_weight("A", "B"), 1.0)
        self.assertEqual(graph.get_weight("B", "A"), 1.0)

    def test_directed_roads_go_one_way(self):
        graph = Graph(directed=True)
        graph.add_location("A")
        graph.add_location("B")
        graph.add_road("A", "B", 3)
        self.assertTrue(graph.has_road("A", "B"))
        self.assertFalse(graph.has_road("B", "A"))

    def test_remove_road_returns_weight(self):
        graph = make_graph()
        self.assertEqual(graph.remove_road("B", "C"), 2.0)
        self.assertFalse(graph.has_road("C", "B"))
        with self.assertRaises(KeyError):
            graph.remove_road("B", "C")

    def test_invalid_input(self):
        graph = make_graph()
        with self.assertRaises(ValueError):
            graph.add_location("A")
        with self.assertRaises(ValueError):
            graph.add_road("A", "C", -1)
        with self.assertRaises(ValueError):
            graph.add_road("A", "A", 1)
        with self.assertRaises(KeyError):
            graph.add_road("A", "Z", 1)
        with self.assertRaises(KeyError):
            graph.neighbors("Z")

    def test_neighbors_is_read_only(self):
        graph = make_graph()
        with self.assertRaises(TypeError):
            graph.neighbors("A")["C"] = 5  # type: ignore[index]

    def test_copy_is_independent(self):
        graph = make_graph()
        clone = graph.copy()
        clone.remove_road("A", "B")
        self.assertTrue(graph.has_road("A", "B"))


class TestLoading(unittest.TestCase):
    DATA = {
        "locations": [{"name": "X", "x": 0, "y": 0}, {"name": "Y", "x": 3, "y": 4}],
        "roads": [{"from": "X", "to": "Y", "distance": 5}],
    }

    def test_graph_from_dict(self):
        graph = graph_from_dict(self.DATA)
        self.assertEqual(graph.get_weight("Y", "X"), 5.0)

    def test_load_json_file(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "map.json"
            path.write_text(json.dumps(self.DATA), encoding="utf-8")
            graph = load_graph_from_json(path)
        self.assertEqual(len(graph), 2)

    def test_sample_map(self):
        graph = load_sample_graph()
        self.assertEqual(len(graph), 10)
        self.assertIn("Home", graph)
        self.assertIn("Airport", graph)


if __name__ == "__main__":
    unittest.main()
