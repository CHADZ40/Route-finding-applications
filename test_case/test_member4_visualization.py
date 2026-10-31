"""Tests for Member 4 - Visualization and user interface."""

import importlib.util
import tempfile
import unittest
import sys
from pathlib import Path

# Lets you run this file directly (e.g. the Run button in VS Code).
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from study_case.member1_graph import load_sample_graph
from study_case.member2_dijkstra import PathResult, dijkstra
from study_case.member4_visualization import format_route

HAS_PLOTTING = all(importlib.util.find_spec(m) for m in ("matplotlib", "networkx"))


class TestFormatRoute(unittest.TestCase):
    def test_found(self):
        text = format_route(PathResult(["A", "B"], 3.0, 2, "Dijkstra"))
        self.assertIn("A -> B", text)
        self.assertIn("3.0 km", text)
        self.assertIn("[Dijkstra]", text)

    def test_not_found(self):
        self.assertIn("No route found", format_route(PathResult([], float("inf"), 1)))


@unittest.skipUnless(HAS_PLOTTING, "matplotlib and networkx are not installed")
class TestDrawing(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        import matplotlib
        matplotlib.use("Agg")

    def tearDown(self):
        import matplotlib.pyplot as plt
        plt.close("all")

    def test_to_networkx(self):
        from study_case.member4_visualization import to_networkx
        graph = load_sample_graph()
        nx_graph = to_networkx(graph)
        self.assertEqual(nx_graph.number_of_nodes(), len(graph))
        self.assertEqual(nx_graph.number_of_edges(), graph.road_count())

    def test_draw_map_and_save(self):
        from study_case.member4_visualization import draw_map, save_figure
        graph = load_sample_graph()
        result = dijkstra(graph, "Home", "Airport")
        fig = draw_map(graph, result.path, blocked=[("Mall", "Hospital")])
        with tempfile.TemporaryDirectory() as tmp:
            path = save_figure(fig, Path(tmp) / "map.png")
            self.assertGreater(path.stat().st_size, 0)

    def test_plot_performance(self):
        from study_case.member3_astar import compare_algorithms
        from study_case.member4_visualization import plot_performance
        rows = compare_algorithms(load_sample_graph(), [("Home", "Airport")], repeats=1)
        fig = plot_performance(rows)
        self.assertEqual(len(fig.axes), 2)


if __name__ == "__main__":
    unittest.main()
