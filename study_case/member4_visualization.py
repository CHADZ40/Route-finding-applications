"""
Noreak - Visualization and user interface
===========================================

Owner: Noreak

Responsibilities
----------------
* ``format_route``      - human-readable text for a ``PathResult``.
* ``to_networkx``       - convert our ``Graph`` into a ``networkx.Graph``.
* ``draw_map``          - draw the map, highlight a route and blocked roads.
* ``plot_performance``  - charts for the Dijkstra vs A* comparison.

``networkx`` and ``matplotlib`` are imported inside the drawing functions so
the text helpers still work when those libraries are not installed.

Tests live in ``test_case/test_member4_visualization.py``.

CHALLENGE
---------
Start with ``format_route`` (no libraries needed), then ``to_networkx``,
then the drawings. Look at your PNGs in ``demonstration/output/``: tests
only check that a picture is saved, YOU check that it looks right.

    python -m unittest test_case.test_member4_visualization -v
"""

from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING, Iterable, Sequence

from study_case.member1_graph import Graph
from study_case.member2_dijkstra import PathResult

if TYPE_CHECKING:
    from matplotlib.figure import Figure
    from study_case.member3_astar import ComparisonRow

# Colors (fixed order, colorblind-checked). Text stays in neutral ink.
ROUTE_COLOR = "#2a78d6"      # blue  - highlighted route
ALT_COLOR = "#eb6834"        # orange - second algorithm / alternative
BLOCKED_COLOR = "#e34948"    # red    - blocked roads (always also dashed + labelled)
ROAD_COLOR = "#c3c2b7"
NODE_COLOR = "#52514e"
TEXT_COLOR = "#0b0b0b"
MUTED_TEXT = "#52514e"
ALGORITHM_COLORS = {"Dijkstra": ROUTE_COLOR, "A*": ALT_COLOR}


def format_route(result: PathResult, unit: str = "km") -> str:
    # Expected output for a found route:
    #   [Dijkstra] Home -> School -> Library -> Hospital -> Airport
    #       distance: 13.1 km | stops: 5 | locations visited: 10
    # TODO 1: label = "[<algorithm>] " if result.algorithm else ""
    # TODO 2: if not result.found:
    #             return f"{label}No route found (visited N locations)"
    # TODO 3: otherwise join the path with " -> " and add a second line with
    #         the distance (1 decimal + unit), number of stops, locations visited
    raise NotImplementedError


def to_networkx(graph: Graph):
    import networkx as nx

    # TODO 1: nx_graph = nx.DiGraph() if graph.directed else nx.Graph()
    # TODO 2: for every location: nx_graph.add_node(name, pos=(x, y))
    # TODO 3: for every road (a, b, weight): nx_graph.add_edge(a, b, weight=weight)
    # TODO 4: return nx_graph
    raise NotImplementedError


def _style_axes(ax) -> None:
    ax.set_axis_off()
    ax.set_aspect("equal")


def draw_map(graph: Graph, path: Sequence[str] | None = None, title: str = "Route Finder Map",
             blocked: Iterable[tuple[str, str]] = (), path_color: str = ROUTE_COLOR,
             show_weights: bool = True, ax=None) -> Figure:
    """Draw every location and road; highlight ``path`` and dashed ``blocked`` roads."""
    import matplotlib.pyplot as plt
    import networkx as nx
    from matplotlib.lines import Line2D

    # Draw in LAYERS - later layers are drawn on top of earlier ones.
    # TODO 1: nx_graph = to_networkx(graph); pos = nx.get_node_attributes(nx_graph, "pos")
    # TODO 2: fig = ax.figure if ax is given, else plt.figure(figsize=(9, 6));
    #         ax = ax or fig.add_subplot()
    # TODO 3: all roads in ROAD_COLOR:   nx.draw_networkx_edges(nx_graph, pos, ax=ax, ...)
    # TODO 4: blocked roads, red + dashed: draw_networkx_edges(nx.Graph(list(blocked)),
    #         pos, ..., style="dashed")
    # TODO 5: the route: edgelist=list(zip(path, path[1:])), thicker line, path_color
    # TODO 6: if show_weights: nx.draw_networkx_edge_labels(...) with a white bbox
    #         so the numbers stay readable on top of the route
    # TODO 7: nodes: nx.draw_networkx_nodes(...) - path_color for places on the
    #         route, NODE_COLOR for the rest
    # TODO 8: place names slightly above each node: nx.draw_networkx_labels(...)
    # TODO 9: a legend built from Line2D handles (Road / Route / Blocked road),
    #         ax.set_title(title), _style_axes(ax), fig.tight_layout()
    # TODO 10: return fig
    raise NotImplementedError


def plot_performance(rows: Sequence[ComparisonRow], title: str = "Dijkstra vs A*") -> Figure:
    """Two small multiples: average time and locations visited, per route."""
    import matplotlib.pyplot as plt

    # TODO 1: routes = unique "start → goal" labels in order;
    #         algorithms = unique algorithm names in order (hint: dict.fromkeys)
    # TODO 2: fig, axes = plt.subplots(1, 2, figsize=(11, 4.5))
    # TODO 3: left chart = avg_ms, right chart = nodes_visited.
    #         Grouped bars: one bar per algorithm for each route, each algorithm
    #         shifted a little left/right; colors from ALGORITHM_COLORS
    # TODO 4: route names as x tick labels, a title and a legend on each chart
    # TODO 5: fig.suptitle(title); fig.tight_layout(); return fig
    # Never put both measures on one chart with two y-axes - that's why we use two.
    raise NotImplementedError


def save_figure(fig: Figure, path: str | Path) -> Path:
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(path, dpi=150, bbox_inches="tight")
    return path
