"""
Member 4 - Visualization and user interface
===========================================

Owner: Member 4

Responsibilities
----------------
* ``format_route``      - human-readable text for a ``PathResult``.
* ``to_networkx``       - convert our ``Graph`` into a ``networkx.Graph``.
* ``draw_map``          - draw the map, highlight a route and blocked roads.
* ``plot_performance``  - charts for the Dijkstra vs A* comparison.

``networkx`` and ``matplotlib`` are imported inside the drawing functions so
the text helpers still work when those libraries are not installed.

Tests live in ``test_case/test_member4_visualization.py``.
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
    label = f"[{result.algorithm}] " if result.algorithm else ""
    if not result.found:
        return f"{label}No route found (visited {result.nodes_visited} locations)"
    return (f"{label}{' -> '.join(result.path)}\n"
            f"    distance: {result.distance:.1f} {unit} | stops: {len(result.path)} | "
            f"locations visited: {result.nodes_visited}")


def to_networkx(graph: Graph):
    import networkx as nx

    nx_graph = nx.DiGraph() if graph.directed else nx.Graph()
    for name in graph.locations:
        loc = graph.location(name)
        nx_graph.add_node(name, pos=(loc.x, loc.y))
    for a, b, weight in graph.roads():
        nx_graph.add_edge(a, b, weight=weight)
    return nx_graph


def _style_axes(ax) -> None:
    ax.set_axis_off()
    ax.set_aspect("equal")


def draw_map(graph: Graph, path: Sequence[str] | None = None, title: str = "Route Finder Map",
             blocked: Iterable[tuple[str, str]] = (), path_color: str = ROUTE_COLOR,
             show_weights: bool = True, ax=None) -> Figure:
    """Draw every location and road; highlight ``path`` and dashed ``blocked`` roads."""
    import matplotlib.pyplot as plt
    import networkx as nx

    nx_graph = to_networkx(graph)
    pos = nx.get_node_attributes(nx_graph, "pos")
    fig = ax.figure if ax is not None else plt.figure(figsize=(9, 6))
    ax = ax or fig.add_subplot()

    nx.draw_networkx_edges(nx_graph, pos, ax=ax, edge_color=ROAD_COLOR, width=2)

    blocked = list(blocked)
    if blocked:
        nx.draw_networkx_edges(nx.Graph(blocked), pos, ax=ax, edge_color=BLOCKED_COLOR,
                               width=2, style="dashed")
    if path and len(path) > 1:
        route_edges = list(zip(path, path[1:]))
        nx.draw_networkx_edges(nx_graph, pos, edgelist=route_edges, ax=ax,
                               edge_color=path_color, width=4)

    if show_weights:
        labels = {(a, b): f"{w:g}" for a, b, w in nx_graph.edges(data="weight")}
        nx.draw_networkx_edge_labels(nx_graph, pos, edge_labels=labels, ax=ax, font_size=8,
                                     font_color=MUTED_TEXT, rotate=False,
                                     bbox={"facecolor": "white", "edgecolor": "none", "pad": 1})

    on_path = set(path or [])
    nx.draw_networkx_nodes(nx_graph, pos, ax=ax, node_size=320, edgecolors="white", linewidths=2,
                           node_color=[path_color if n in on_path else NODE_COLOR for n in nx_graph])
    label_pos = {n: (x, y + 0.32) for n, (x, y) in pos.items()}
    nx.draw_networkx_labels(nx_graph, label_pos, ax=ax, font_size=9, font_color=TEXT_COLOR)

    # Legend so identity never relies on color alone.
    from matplotlib.lines import Line2D
    handles = [Line2D([], [], color=ROAD_COLOR, lw=2, label="Road")]
    if path:
        handles.append(Line2D([], [], color=path_color, lw=4, label="Route"))
    if blocked:
        handles.append(Line2D([], [], color=BLOCKED_COLOR, lw=2, ls="--", label="Blocked road"))
    ax.legend(handles=handles, loc="lower right", frameon=False)
    ax.set_title(title, color=TEXT_COLOR, loc="left")
    _style_axes(ax)
    fig.tight_layout()
    return fig


def plot_performance(rows: Sequence[ComparisonRow], title: str = "Dijkstra vs A*") -> Figure:
    """Two small multiples: average time and locations visited, per route."""
    import matplotlib.pyplot as plt

    routes = list(dict.fromkeys(f"{r.start} → {r.goal}" for r in rows))
    algorithms = list(dict.fromkeys(r.algorithm for r in rows))
    fig, axes = plt.subplots(1, 2, figsize=(11, 4.5))
    width = 0.8 / len(algorithms)

    for ax, metric, label in ((axes[0], "avg_ms", "Average time (ms)"),
                              (axes[1], "nodes_visited", "Locations visited")):
        for i, algorithm in enumerate(algorithms):
            values = [getattr(r, metric) for r in rows if r.algorithm == algorithm]
            xs = [x + (i - (len(algorithms) - 1) / 2) * width for x in range(len(routes))]
            ax.bar(xs, values, width * 0.92, label=algorithm,
                   color=ALGORITHM_COLORS.get(algorithm, NODE_COLOR))
        ax.set_xticks(range(len(routes)), routes, rotation=20, ha="right", fontsize=8)
        ax.set_title(label, color=TEXT_COLOR, loc="left")
        ax.grid(axis="y", color="#e5e4df", linewidth=0.8)
        ax.set_axisbelow(True)
        for side in ("top", "right"):
            ax.spines[side].set_visible(False)
        ax.legend(frameon=False)
    fig.suptitle(title, color=TEXT_COLOR, x=0.01, ha="left")
    fig.tight_layout()
    return fig


def save_figure(fig: Figure, path: str | Path) -> Path:
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(path, dpi=150, bbox_inches="tight")
    return path
