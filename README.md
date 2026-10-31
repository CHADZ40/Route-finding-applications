# Route Finder

A Python route-finding application, similar to a simplified Google Maps,
that calculates the shortest path between two locations. The map is modeled
as a weighted graph where locations are nodes and roads are edges weighted
by distance (km).

## Features
- Weighted graph stored as an adjacency list
- Dijkstra's algorithm using a min-heap priority queue (`heapq`)
- A* search with a straight-line (Euclidean) heuristic
- Performance comparison of Dijkstra vs A* on a large random grid city
- Road blocking and traffic simulation (re-routing around closed roads)
- Route visualization with `networkx` and `matplotlib`
- Interactive command-line prototype

## Data Structures and Concepts
- Graph (adjacency list: `dict[str, dict[str, float]]`)
- Priority queue / min-heap (`heapq`)
- Dictionaries and sets

## Advanced Python Used
- Object-oriented design with a custom `Graph` class
- Type hints
- Dataclasses (`Location`, `PathResult`, `ComparisonRow`)
- Decorators (`@timed` for benchmarking)
- Context managers (`blocked_roads` temporarily closes roads)
- Unit testing with `unittest`

## Project Structure

```
Final-project/
├── study_case/                      # each member builds their own task here
│   ├── data/sample_map.json         # 10-location "Sample City" map
│   ├── member1_graph.py             # Graph class and data loading
│   ├── member2_dijkstra.py          # Dijkstra's algorithm
│   ├── member3_astar.py             # A* and performance comparison
│   ├── member4_visualization.py     # Visualization and user interface
│   └── member5_road_blocking.py     # Road blocking and traffic simulation
├── test_case/                       # tests to check each member's work
│   ├── test_member1_graph.py
│   ├── test_member2_dijkstra.py
│   ├── test_member3_astar.py
│   ├── test_member4_visualization.py
│   └── test_member5_road_blocking.py
├── demonstration/
│   ├── main.py                      # runs everything: results, graphs, prototype
│   └── output/                      # generated PNG graphs (git-ignored)
├── requirements.txt
├── LICENSE
└── README.md
```

## Getting Started
Requires Python 3.10 or newer.

    git clone <your-repo-url>
    cd Final-project
    pip install -r requirements.txt

Run everything from the project root:

    python demonstration/main.py                 # full demonstration + graphs
    python demonstration/main.py --no-show       # same, but only save the PNGs
    python demonstration/main.py --interactive   # interactive route-finder prototype
    python demonstration/main.py --test          # run every test case

    python -m unittest -v                                    # all tests
    python -m unittest test_case.test_member2_dijkstra -v    # one member's tests

## What the Demonstration Shows
1. The Sample City map printed as an adjacency list
2. Shortest route Home → Airport with Dijkstra, plus distances to every location
3. The same route with A*, and a benchmark on a 40×40 grid city (time and locations visited)
4. A blocked road on the best route and the detour found around it, plus a traffic example
5. Graphs saved to `demonstration/output/`:
   `1_map.png`, `2_shortest_route.png`, `3_blocked_route.png`, `4_performance.png`

## Team Workflow
1. Work only in your own file in `study_case/` and your own test file in `test_case/`.
2. Keep the public function names the same — other members and `main.py` import them.
3. Before pushing, run your tests and the full suite: `python -m unittest -v`.
4. Run `python demonstration/main.py` to make sure everything still works together.
5. Use a branch per member (e.g. `member2-dijkstra`) and open a pull request into `main`.

## Team
| Member | Task | Study case | Test case |
|---|---|---|---|
| Seth | Graph class and data loading | `member1_graph.py` | `test_member1_graph.py` |
| Menghour | Dijkstra's algorithm | `member2_dijkstra.py` | `test_member2_dijkstra.py` |
| Kheang | A* and performance comparison | `member3_astar.py` | `test_member3_astar.py` |
| Noreak | Visualization and user interface | `member4_visualization.py` | `test_member4_visualization.py` |
| Raboth | Road blocking and traffic simulation | `member5_road_blocking.py` | `test_member5_road_blocking.py` |

## Course
Computer Science B: Data Structures and Advanced Python

## License
MIT — see [LICENSE](LICENSE).
