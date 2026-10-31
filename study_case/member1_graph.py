"""
Member 1 - Graph class and data loading
=======================================

Owner: Member 1

Responsibilities
----------------
* ``Location``  - a dataclass for a place on the map (name + x/y coordinates).
* ``Graph``     - a weighted graph stored as an adjacency list.
* Loading a map from a JSON file (see ``data/sample_map.json``).

Every other module builds on the ``Graph`` API defined here, so keep the
public method names stable. Tests live in ``test_case/test_member1_graph.py``.

CHALLENGE
---------
Replace every ``raise NotImplementedError`` with real code, following the
TODO hints. You are done when this passes:

    python -m unittest test_case.test_member1_graph -v

Everyone else depends on this file, so finish it first!
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from types import MappingProxyType
from typing import Any, Iterator, Mapping

DATA_DIR = Path(__file__).resolve().parent / "data"
SAMPLE_MAP = DATA_DIR / "sample_map.json"


@dataclass(frozen=True)
class Location:
    """A node on the map. Coordinates are used by A* and by the visualizer."""

    name: str
    x: float = 0.0
    y: float = 0.0


class Graph:
    """Weighted graph stored as an adjacency list: ``{node: {neighbor: weight}}``.

    Roads are undirected by default (two-way streets). Weights must be
    non-negative, which is what Dijkstra's algorithm requires.
    """

    def __init__(self, directed: bool = False) -> None:
        self.directed = directed
        self._adj: dict[str, dict[str, float]] = {}
        self._locations: dict[str, Location] = {}

    # ----- locations -------------------------------------------------------
    def add_location(self, name: str, x: float = 0.0, y: float = 0.0) -> Location:
        # TODO 1: if name is already in self._locations -> raise ValueError
        # TODO 2: create a Location (convert x and y with float())
        # TODO 3: store it in self._locations[name] and give it an empty
        #         neighbor dict in self._adj[name]
        # TODO 4: return the Location
        raise NotImplementedError

    def location(self, name: str) -> Location:
        self._require(name)
        return self._locations[name]

    @property
    def locations(self) -> list[str]:
        return list(self._adj)

    # ----- roads -----------------------------------------------------------
    def add_road(self, a: str, b: str, weight: float) -> None:
        # TODO 1: both a and b must exist -> use self._require()
        # TODO 2: a == b -> raise ValueError (a road needs two different places)
        # TODO 3: weight < 0 -> raise ValueError (Dijkstra can't handle it. Why?)
        # TODO 4: store the weight as a float in self._adj[a][b]
        # TODO 5: if the graph is NOT directed, also store self._adj[b][a]
        raise NotImplementedError

    def remove_road(self, a: str, b: str) -> float:
        """Remove the road and return its weight (so it can be restored)."""
        # TODO 1: no road from a to b -> raise KeyError
        # TODO 2: pop b out of self._adj[a] and keep the weight
        # TODO 3: if NOT directed, also remove a from self._adj[b]
        # TODO 4: return the weight (Member 5 uses it to put the road back)
        raise NotImplementedError

    def has_road(self, a: str, b: str) -> bool:
        # TODO: True if b is a neighbor of a. Must NOT crash when a is unknown
        #       (hint: dict.get with a default)
        raise NotImplementedError

    def get_weight(self, a: str, b: str) -> float:
        # TODO: raise KeyError if there is no road, otherwise return its weight
        raise NotImplementedError

    def neighbors(self, name: str) -> Mapping[str, float]:
        """Read-only view of ``{neighbor: weight}`` for ``name``."""
        # TODO 1: check the location exists (self._require)
        # TODO 2: return MappingProxyType(...) of its neighbor dict, so other
        #         code can read it but can't change the map by accident
        raise NotImplementedError

    def roads(self) -> Iterator[tuple[str, str, float]]:
        """Yield every road once as ``(a, b, weight)``."""
        # TODO 1: loop over every (a, neighbors) in self._adj, and every (b, weight)
        # TODO 2: in an undirected graph A-B is stored twice (A->B and B->A).
        #         Yield it only once: remember frozenset((a, b)) in a set
        #         and skip pairs you have already seen
        # TODO 3: yield a, b, weight   (this makes roads() a generator)
        raise NotImplementedError

    def road_count(self) -> int:
        return sum(1 for _ in self.roads())

    # ----- helpers ---------------------------------------------------------
    def copy(self) -> Graph:
        # TODO 1: make a new Graph with the same `directed` value
        # TODO 2: add every location (same name, x, y)
        # TODO 3: add every road from self.roads()
        # TODO 4: return it. Changing the copy must not change the original!
        raise NotImplementedError

    def _require(self, name: str) -> None:
        if name not in self._adj:
            raise KeyError(f"Unknown location: '{name}'")

    def __contains__(self, name: object) -> bool:
        return name in self._adj

    def __len__(self) -> int:
        return len(self._adj)

    def __repr__(self) -> str:
        kind = "directed" if self.directed else "undirected"
        return f"Graph({len(self)} locations, {self.road_count()} roads, {kind})"


# ----- data loading --------------------------------------------------------
def graph_from_dict(data: Mapping[str, Any]) -> Graph:
    """Build a graph from ``{"locations": [...], "roads": [...]}``."""
    # TODO 1: graph = Graph(directed=data.get("directed", False))
    # TODO 2: for each item in data["locations"]: add_location(name, x, y)
    #         (x and y may be missing -> default to 0.0)
    # TODO 3: for each item in data["roads"]: add_road(from, to, distance)
    # TODO 4: return the graph
    # Open study_case/data/sample_map.json to see the exact key names.
    raise NotImplementedError


def load_graph_from_json(path: str | Path) -> Graph:
    # TODO: open the file (encoding="utf-8"), json.load it,
    #       and return graph_from_dict(...)
    raise NotImplementedError


def load_sample_graph() -> Graph:
    """The 10-location 'Sample City' map used by the demonstration."""
    return load_graph_from_json(SAMPLE_MAP)
