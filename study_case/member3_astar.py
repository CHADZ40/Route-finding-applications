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
    la, lb = graph.location(a), graph.location(b)
    return math.hypot(la.x - lb.x, la.y - lb.y)


def zero_heuristic(graph: Graph, a: str, b: str) -> float:
    """With this heuristic A* behaves exactly like Dijkstra."""
    return 0.0


def astar(graph: Graph, start: str, goal: str, heuristic: Heuristic = euclidean_heuristic) -> PathResult:
    check_endpoints(graph, start, goal)
    g_score: dict[str, float] = {start: 0.0}
    previous: dict[str, str] = {}
    closed: set[str] = set()
    heap: list[tuple[float, float, str]] = [(heuristic(graph, start, goal), 0.0, start)]

    while heap:
        _, g, node = heapq.heappop(heap)
        if node in closed:
            continue
        closed.add(node)
        if node == goal:
            return PathResult(reconstruct_path(previous, start, goal), g, len(closed), "A*")
        for nbr, weight in graph.neighbors(node).items():
            new_g = g + weight
            if new_g < g_score.get(nbr, math.inf):
                g_score[nbr] = new_g
                previous[nbr] = node
                heapq.heappush(heap, (new_g + heuristic(graph, nbr, goal), new_g, nbr))

    return PathResult([], math.inf, len(closed), "A*")


def timed(func: Callable[..., T]) -> Callable[..., tuple[T, float]]:
    """Decorator: the wrapped function returns ``(result, elapsed_seconds)``."""

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        result = func(*args, **kwargs)
        return result, time.perf_counter() - start

    return wrapper


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
    rows: list[ComparisonRow] = []
    for start, goal in pairs:
        for name, algorithm in ALGORITHMS.items():
            run = timed(algorithm)
            total = 0.0
            for _ in range(repeats):
                result, elapsed = run(graph, start, goal)
                total += elapsed
            rows.append(ComparisonRow(start, goal, name, result.distance, result.nodes_visited,
                                      total / repeats * 1000))
    return rows


def generate_grid_graph(rows: int, cols: int, seed: int | None = None, max_detour: float = 1.5) -> Graph:
    """A ``rows x cols`` grid city. Node ``"r,c"`` sits at ``(x=c, y=r)``.

    Each road is 1-``max_detour`` times its straight-line length, so the
    Euclidean heuristic stays admissible.
    """
    rng = random.Random(seed)
    graph = Graph()
    for r in range(rows):
        for c in range(cols):
            graph.add_location(f"{r},{c}", c, r)
    for r in range(rows):
        for c in range(cols):
            if c + 1 < cols:
                graph.add_road(f"{r},{c}", f"{r},{c + 1}", round(rng.uniform(1, max_detour), 3))
            if r + 1 < rows:
                graph.add_road(f"{r},{c}", f"{r + 1},{c}", round(rng.uniform(1, max_detour), 3))
    return graph
