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

CHALLENGE
---------
Before coding, run Dijkstra BY HAND on the Sample City map from Home to
Airport (see the team guide). The answer must be 13.1 km via School,
Library and Hospital. You are done when this passes:

    python -m unittest test_case.test_member2_dijkstra -v
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
    # `previous` maps each place to the place we came from,
    # e.g. {"B": "A", "C": "B"} means A -> B -> C.
    # TODO 1: if goal != start and goal is not in previous -> return [] (no route)
    # TODO 2: start a list with [goal]
    # TODO 3: while the last item is not start: append previous[last item]
    # TODO 4: the list is backwards (goal ... start) -> reverse it and return
    raise NotImplementedError


def check_endpoints(graph: Graph, start: str, goal: str) -> None:
    for name in (start, goal):
        if name not in graph:
            raise KeyError(f"Unknown location: '{name}'")


def dijkstra(graph: Graph, start: str, goal: str) -> PathResult:
    """Shortest path from ``start`` to ``goal`` (stops as soon as goal is settled)."""
    check_endpoints(graph, start, goal)
    # TODO 1: set up
    #         dist = {start: 0.0}      best distance found so far
    #         previous = {}            where we came from
    #         visited = set()          places whose distance is final
    #         heap = [(0.0, start)]    (distance, place) pairs
    # TODO 2: while heap is not empty:
    #         d, node = heapq.heappop(heap)
    # TODO 3: if node is already visited -> continue
    #         (it is an old, longer entry. Why is skipping it safe?)
    # TODO 4: add node to visited. If node == goal -> break
    # TODO 5: for nbr, weight in graph.neighbors(node).items():
    #             new_dist = d + weight
    #             if new_dist < dist.get(nbr, math.inf):
    #                 update dist[nbr], previous[nbr] and heappush (new_dist, nbr)
    # TODO 6: if goal was never visited:
    #             return PathResult([], math.inf, len(visited), "Dijkstra")
    #         else return PathResult(reconstruct_path(...), dist[goal],
    #                                len(visited), "Dijkstra")
    raise NotImplementedError


def shortest_distances(graph: Graph, start: str) -> dict[str, float]:
    """Distance from ``start`` to every location (``math.inf`` if unreachable)."""
    check_endpoints(graph, start, start)
    # TODO 1: dist = {every location: math.inf}, then dist[start] = 0.0
    # TODO 2: same heap loop as dijkstra, but never stop early and no `previous`
    #         (instead of a visited set you can skip entries where d > dist[node])
    # TODO 3: return dist
    raise NotImplementedError
