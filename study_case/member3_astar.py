"""
Member 3 - A* algorithm and performance comparison
==================================================

Owner: Member 3

Responsibilities
----------------
* ``astar``                - A* search guided by a straight-line heuristic.
* ``timed``                - decorator that measures how long a call takes.
* ``compare_algorithms``   - benchmark Dijkstra vs A* on the same routes.
* ``generate_grid_graph``  - a bigger random map so the comparison is meaningful.

A* is only guaranteed to find the shortest path when the heuristic never
overestimates, i.e. every road is at least as long as the straight line
between its two ends. The sample map and the grid generator respect this.

Tests live in ``test_case/test_member3_astar.py``.

CHALLENGE
---------
A* needs Member 2's Dijkstra working first (the tests compare against it).
You are done when this passes:

    python -m unittest test_case.test_member3_astar -v
"""

from __future__ import annotations

import functools
import heapq
import math
import random
import time
from dataclasses import dataclass
from typing import Callable, Iterable, TypeVar

from study_case.member1_graph import Graph
from study_case.member2_dijkstra import PathResult, check_endpoints, dijkstra, reconstruct_path

Heuristic = Callable[[Graph, str, str], float]
T = TypeVar("T")


def euclidean_heuristic(graph: Graph, a: str, b: str) -> float:
    # TODO: get both Locations with graph.location(...) and return the
    #       straight-line distance between them (hint: math.hypot(dx, dy))
    raise NotImplementedError


def zero_heuristic(graph: Graph, a: str, b: str) -> float:
    """With this heuristic A* behaves exactly like Dijkstra."""
    return 0.0


def astar(graph: Graph, start: str, goal: str, heuristic: Heuristic = euclidean_heuristic) -> PathResult:
    check_endpoints(graph, start, goal)
    # A* = Dijkstra, but the heap is sorted by f = g + h:
    #   g = real distance from start so far
    #   h = heuristic(graph, node, goal) = guess of the distance left
    # TODO 1: g_score = {start: 0.0}, previous = {}, closed = set()
    #         heap = [(heuristic(graph, start, goal), 0.0, start)]   # (f, g, node)
    # TODO 2: while heap: f, g, node = heapq.heappop(heap)
    # TODO 3: skip nodes already in closed, otherwise add node to closed
    # TODO 4: if node == goal: return PathResult(reconstruct_path(...), g,
    #                                            len(closed), "A*")
    # TODO 5: for each neighbor: new_g = g + weight
    #         if new_g < g_score.get(nbr, math.inf):
    #             update g_score and previous, then push
    #             (new_g + heuristic(graph, nbr, goal), new_g, nbr)
    # TODO 6: heap is empty -> no route: PathResult([], math.inf, len(closed), "A*")
    raise NotImplementedError


def timed(func: Callable[..., T]) -> Callable[..., tuple[T, float]]:
    """Decorator: the wrapped function returns ``(result, elapsed_seconds)``."""
    # TODO 1: define wrapper(*args, **kwargs) and put @functools.wraps(func) on it
    # TODO 2: inside: start = time.perf_counter(), call func, measure the time
    # TODO 3: wrapper returns (result, elapsed_seconds)
    # TODO 4: timed returns wrapper
    raise NotImplementedError


@dataclass
class ComparisonRow:
    start: str
    goal: str
    algorithm: str
    distance: float
    nodes_visited: int
    avg_ms: float


ALGORITHMS: dict[str, Callable[[Graph, str, str], PathResult]] = {
    "Dijkstra": dijkstra,
    "A*": astar,
}


def compare_algorithms(graph: Graph, pairs: Iterable[tuple[str, str]], repeats: int = 5) -> list[ComparisonRow]:
    """Run every algorithm on every ``(start, goal)`` pair and average the time."""
    # TODO 1: rows = []
    # TODO 2: for each (start, goal) in pairs, for each (name, algorithm) in ALGORITHMS:
    #         run = timed(algorithm)
    #         call run(graph, start, goal) `repeats` times and add up the seconds
    # TODO 3: append ComparisonRow(start, goal, name, result.distance,
    #         result.nodes_visited, average time in MILLISECONDS)
    # TODO 4: return rows  (order: Dijkstra row, then A* row, for each pair)
    raise NotImplementedError


def generate_grid_graph(rows: int, cols: int, seed: int | None = None, max_detour: float = 1.5) -> Graph:
    """A ``rows x cols`` grid city. Node ``"r,c"`` sits at ``(x=c, y=r)``.

    Each road is 1-``max_detour`` times its straight-line length, so the
    Euclidean heuristic stays admissible.
    """
    # TODO 1: rng = random.Random(seed)   (same seed -> same map every time)
    # TODO 2: add a location named f"{r},{c}" at x=c, y=r for every cell
    # TODO 3: connect each cell to its right neighbor (c + 1) and the one
    #         below (r + 1) when they exist, with weight
    #         round(rng.uniform(1, max_detour), 3)
    # TODO 4: return the graph
    raise NotImplementedError
