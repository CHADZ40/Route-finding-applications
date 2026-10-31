"""
Member 2 - Dijkstra's algorithm
===============================

Owner: Member 2

Responsibilities
----------------
* ``PathResult``          - the result object shared by every algorithm.
* ``dijkstra``            - shortest path between two locations using a
                            min-heap priority queue (``heapq``).
* ``shortest_distances``  - distance from one location to every other one.

Tests live in ``test_case/test_member2_dijkstra.py``.
"""

from __future__ import annotations

import heapq
import math
from dataclasses import dataclass

from study_case.member1_graph import Graph


@dataclass
class PathResult:
    """Outcome of a route search. An empty ``path`` means no route exists."""

    path: list[str]
    distance: float
    nodes_visited: int = 0
    algorithm: str = ""

    @property
    def found(self) -> bool:
        return bool(self.path)


def reconstruct_path(previous: dict[str, str], start: str, goal: str) -> list[str]:
    """Walk the ``previous`` links back from ``goal`` to ``start``."""
    if goal != start and goal not in previous:
        return []
    path = [goal]
    while path[-1] != start:
        path.append(previous[path[-1]])
    path.reverse()
    return path


def check_endpoints(graph: Graph, start: str, goal: str) -> None:
    for name in (start, goal):
        if name not in graph:
            raise KeyError(f"Unknown location: '{name}'")


def dijkstra(graph: Graph, start: str, goal: str) -> PathResult:
    """Shortest path from ``start`` to ``goal`` (stops as soon as goal is settled)."""
    check_endpoints(graph, start, goal)
    dist: dict[str, float] = {start: 0.0}
    previous: dict[str, str] = {}
    visited: set[str] = set()
    heap: list[tuple[float, str]] = [(0.0, start)]

    while heap:
        d, node = heapq.heappop(heap)
        if node in visited:
            continue  # stale heap entry
        visited.add(node)
        if node == goal:
            break
        for nbr, weight in graph.neighbors(node).items():
            new_dist = d + weight
            if new_dist < dist.get(nbr, math.inf):
                dist[nbr] = new_dist
                previous[nbr] = node
                heapq.heappush(heap, (new_dist, nbr))

    if goal not in visited:
        return PathResult([], math.inf, len(visited), "Dijkstra")
    return PathResult(reconstruct_path(previous, start, goal), dist[goal], len(visited), "Dijkstra")


def shortest_distances(graph: Graph, start: str) -> dict[str, float]:
    """Distance from ``start`` to every location (``math.inf`` if unreachable)."""
    check_endpoints(graph, start, start)
    dist = {name: math.inf for name in graph.locations}
    dist[start] = 0.0
    heap: list[tuple[float, str]] = [(0.0, start)]
    while heap:
        d, node = heapq.heappop(heap)
        if d > dist[node]:
            continue
        for nbr, weight in graph.neighbors(node).items():
            if d + weight < dist[nbr]:
                dist[nbr] = d + weight
                heapq.heappush(heap, (dist[nbr], nbr))
    return dist
