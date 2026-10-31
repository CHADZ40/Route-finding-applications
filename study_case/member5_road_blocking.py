"""
Member 5 - Road blocking and traffic simulation
===============================================

Owner: Member 5

Responsibilities
----------------
* ``blocked_roads``        - context manager that closes roads temporarily
                             and always reopens them afterwards.
* ``find_route_avoiding``  - re-route around closed roads.
* ``apply_traffic``        - a copy of the map with slower (longer) roads.
* ``compare_routes``       - how much a detour costs.

Tests live in ``test_case/test_member5_road_blocking.py``.

CHALLENGE
---------
Needs Member 1's Graph (remove_road / add_road / copy) and Member 2's
Dijkstra. You are done when this passes:

    python -m unittest test_case.test_member5_road_blocking -v
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
    # Usage:
    #     with blocked_roads(graph, [("Library", "Hospital")]):
    #         ...the road is closed here...
    #     ...and open again here, even if an error happened inside!
    # TODO 1: removed = []   - remember (a, b, weight) for every road you remove
    # TODO 2: try:
    #             for each (a, b): weight = graph.remove_road(a, b); remember it
    #             yield graph
    #         finally:
    #             put every removed road back with graph.add_road(a, b, weight)
    # Think: why must the removing loop be INSIDE the try? (see the test
    # test_blocking_missing_road_restores_earlier_ones)
    raise NotImplementedError
    yield graph  # keeps this a generator until you write it; delete this line


def find_route_avoiding(graph: Graph, start: str, goal: str, blocked: Iterable[Road],
                        algorithm: Callable[[Graph, str, str], PathResult] = dijkstra) -> PathResult:
    # TODO: inside `with blocked_roads(graph, blocked):` return algorithm(graph, start, goal)
    raise NotImplementedError


def apply_traffic(graph: Graph, factors: Mapping[Road, float]) -> Graph:
    """Return a copy where each listed road's weight is multiplied by its factor.

    Factors must be >= 1 (traffic only slows you down), which also keeps the
    A* straight-line heuristic valid.
    """
    # TODO 1: slowed = graph.copy()   - NEVER change the original map
    # TODO 2: for each (a, b), factor: factor < 1 -> raise ValueError
    # TODO 3: slowed.add_road(a, b, original weight * factor)
    #         (add_road on an existing road overwrites its weight)
    # TODO 4: return slowed
    raise NotImplementedError


def compare_routes(original: PathResult, alternative: PathResult) -> dict[str, float]:
    # TODO: return {"original": ..., "alternative": ..., "extra": ..., "percent": ...}
    #       extra   = alternative distance - original distance
    #       percent = extra / original distance * 100   (0.0 if original is 0)
    raise NotImplementedError
