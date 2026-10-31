"""
Raboth - Road blocking and traffic simulation
===============================================

Owner: Raboth

Responsibilities
----------------
* ``blocked_roads``        - context manager that closes roads temporarily
                             and always reopens them afterwards.
* ``find_route_avoiding``  - re-route around closed roads.
* ``apply_traffic``        - a copy of the map with slower (longer) roads.
* ``compare_routes``       - how much a detour costs.

Tests live in ``test_case/test_member5_road_blocking.py``.
"""

from __future__ import annotations

from contextlib import contextmanager
from typing import Callable, Iterable, Iterator, Mapping

from study_case.member1_graph import Graph
from study_case.member2_dijkstra import PathResult, dijkstra

Road = tuple[str, str]


@contextmanager
def blocked_roads(graph: Graph, roads: Iterable[Road]) -> Iterator[Graph]:
    """Temporarily remove ``roads`` from ``graph``; they are restored on exit."""
    removed: list[tuple[str, str, float]] = []
    try:
        for a, b in roads:
            removed.append((a, b, graph.remove_road(a, b)))
        yield graph
    finally:
        for a, b, weight in removed:
            graph.add_road(a, b, weight)


def find_route_avoiding(graph: Graph, start: str, goal: str, blocked: Iterable[Road],
                        algorithm: Callable[[Graph, str, str], PathResult] = dijkstra) -> PathResult:
    with blocked_roads(graph, blocked):
        return algorithm(graph, start, goal)


def apply_traffic(graph: Graph, factors: Mapping[Road, float]) -> Graph:
    """Return a copy where each listed road's weight is multiplied by its factor.

    Factors must be >= 1 (traffic only slows you down), which also keeps the
    A* straight-line heuristic valid.
    """
    slowed = graph.copy()
    for (a, b), factor in factors.items():
        if factor < 1:
            raise ValueError("Traffic factor must be >= 1")
        slowed.add_road(a, b, graph.get_weight(a, b) * factor)
    return slowed


def compare_routes(original: PathResult, alternative: PathResult) -> dict[str, float]:
    extra = alternative.distance - original.distance
    percent = extra / original.distance * 100 if original.distance else 0.0
    return {"original": original.distance, "alternative": alternative.distance,
            "extra": extra, "percent": percent}
