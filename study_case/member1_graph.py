"""
Seth - Graph class and data loading
=======================================

Owner: Seth

Responsibilities
----------------
* ``Location``  - a dataclass for a place on the map (name + x/y coordinates).
* ``Graph``     - a weighted graph stored as an adjacency list.
* Loading a map from a JSON file (see ``data/sample_map.json``).

Every other module builds on the ``Graph`` API defined here, so keep the
public method names stable. Tests live in ``test_case/test_member1_graph.py``.
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
        if name in self._locations:
            raise ValueError(f"Location '{name}' already exists")
        location = Location(name, float(x), float(y))
        self._locations[name] = location
        self._adj[name] = {}
        return location

    def location(self, name: str) -> Location:
        self._require(name)
        return self._locations[name]

    @property
    def locations(self) -> list[str]:
        return list(self._adj)

    # ----- roads -----------------------------------------------------------
    def add_road(self, a: str, b: str, weight: float) -> None:
        self._require(a)
        self._require(b)
        if a == b:
            raise ValueError("A road must connect two different locations")
        if weight < 0:
            raise ValueError("Road weight must be non-negative")
        self._adj[a][b] = float(weight)
        if not self.directed:
            self._adj[b][a] = float(weight)

    def remove_road(self, a: str, b: str) -> float:
        """Remove the road and return its weight (so it can be restored)."""
        if not self.has_road(a, b):
            raise KeyError(f"No road between '{a}' and '{b}'")
        weight = self._adj[a].pop(b)
        if not self.directed:
            self._adj[b].pop(a, None)
        return weight

    def has_road(self, a: str, b: str) -> bool:
        return b in self._adj.get(a, {})

    def get_weight(self, a: str, b: str) -> float:
        if not self.has_road(a, b):
            raise KeyError(f"No road between '{a}' and '{b}'")
        return self._adj[a][b]

    def neighbors(self, name: str) -> Mapping[str, float]:
        """Read-only view of ``{neighbor: weight}`` for ``name``."""
        self._require(name)
        return MappingProxyType(self._adj[name])

    def roads(self) -> Iterator[tuple[str, str, float]]:
        """Yield every road once as ``(a, b, weight)``."""
        seen: set[frozenset[str]] = set()
        for a, nbrs in self._adj.items():
            for b, weight in nbrs.items():
                if not self.directed:
                    key = frozenset((a, b))
                    if key in seen:
                        continue
                    seen.add(key)
                yield a, b, weight

    def road_count(self) -> int:
        return sum(1 for _ in self.roads())

    # ----- helpers ---------------------------------------------------------
    def copy(self) -> Graph:
        clone = Graph(self.directed)
        for loc in self._locations.values():
            clone.add_location(loc.name, loc.x, loc.y)
        for a, b, weight in self.roads():
            clone.add_road(a, b, weight)
        return clone

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
    graph = Graph(directed=data.get("directed", False))
    for loc in data["locations"]:
        graph.add_location(loc["name"], loc.get("x", 0.0), loc.get("y", 0.0))
    for road in data["roads"]:
        graph.add_road(road["from"], road["to"], road["distance"])
    return graph


def load_graph_from_json(path: str | Path) -> Graph:
    with open(path, encoding="utf-8") as f:
        return graph_from_dict(json.load(f))


def load_sample_graph() -> Graph:
    """The 10-location 'Sample City' map used by the demonstration."""
    return load_graph_from_json(SAMPLE_MAP)
