"""
Route Finder - Demonstration
============================

Brings every team member's work together:

    1. Map loading (Graph)               - Member 1
    2. Dijkstra's shortest path          - Member 2
    3. A* and performance comparison     - Member 3
    4. Road blocking and traffic         - Member 5
    5. Graphs / visualization            - Member 4
    6. Interactive prototype (CLI)       - Member 4 + everyone

Usage (from the project root):

    python demonstration/main.py                 # full demo, opens the graphs
    python demonstration/main.py --no-show       # full demo, only saves PNGs
    python demonstration/main.py --interactive   # route-finder prototype
    python demonstration/main.py --test          # run every test case
"""

from __future__ import annotations

import argparse
import importlib.util
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUTPUT_DIR = Path(__file__).resolve().parent / "output"
sys.path.insert(0, str(ROOT))

from study_case.member1_graph import Graph, load_sample_graph  # noqa: E402
from study_case.member2_dijkstra import PathResult, dijkstra, shortest_distances  # noqa: E402
from study_case.member3_astar import (ComparisonRow, astar, compare_algorithms,  # noqa: E402
                                      generate_grid_graph)
from study_case.member4_visualization import format_route  # noqa: E402
from study_case.member5_road_blocking import (apply_traffic, compare_routes,  # noqa: E402
                                              find_route_avoiding)

HAS_PLOTTING = all(importlib.util.find_spec(m) for m in ("matplotlib", "networkx"))
START, GOAL = "Home", "Airport"


def section(title: str) -> None:
    print(f"\n{'=' * 64}\n  {title}\n{'=' * 64}")


# ----- 1. Graph ------------------------------------------------------------
def demo_graph(graph: Graph) -> None:
    section("1. Map loaded as a weighted graph (adjacency list)  - Member 1")
    print(graph)
    for name in graph.locations:
        roads = ", ".join(f"{n} ({w:g} km)" for n, w in graph.neighbors(name).items())
        print(f"  {name:<9} -> {roads}")


# ----- 2. Dijkstra ---------------------------------------------------------
def demo_dijkstra(graph: Graph) -> PathResult:
    section("2. Dijkstra's algorithm with a min-heap  - Member 2")
    result = dijkstra(graph, START, GOAL)
    print(format_route(result))
    print(f"\n  Distance from {START} to every location:")
    for name, dist in sorted(shortest_distances(graph, START).items(), key=lambda kv: kv[1]):
        print(f"    {name:<9} {dist:5.1f} km")
    return result


# ----- 3. A* + performance -------------------------------------------------
def demo_astar(graph: Graph, dijkstra_result: PathResult) -> tuple[PathResult, list[ComparisonRow]]:
    section("3. A* search and performance comparison  - Member 3")
    result = astar(graph, START, GOAL)
    print(format_route(result))
    same = abs(result.distance - dijkstra_result.distance) < 1e-9
    print(f"  Same distance as Dijkstra: {'yes' if same else 'NO'}")

    grid = generate_grid_graph(40, 40, seed=42)
    pairs = [("0,0", "39,39"), ("0,0", "20,20"), ("10,5", "30,35"), ("39,0", "0,39"), ("5,5", "8,9")]
    print(f"\n  Benchmark on a random {grid}")
    rows = compare_algorithms(grid, pairs, repeats=5)
    print(f"  {'route':<16}{'algorithm':<10}{'distance':>10}{'visited':>9}{'avg ms':>9}")
    for r in rows:
        print(f"  {r.start + ' → ' + r.goal:<16}{r.algorithm:<10}{r.distance:>10.2f}"
              f"{r.nodes_visited:>9}{r.avg_ms:>9.3f}")
    return result, rows


# ----- 4. Road blocking ----------------------------------------------------
def demo_road_blocking(graph: Graph, original: PathResult) -> tuple[list[tuple[str, str]], PathResult]:
    section("4. Road blocking and traffic  - Member 5")
    # Close the middle road of the current best route to force a detour.
    edges = list(zip(original.path, original.path[1:]))
    blocked = [edges[len(edges) // 2]]
    detour = find_route_avoiding(graph, START, GOAL, blocked)
    print(f"  Blocked road: {blocked[0][0]} - {blocked[0][1]}")
    print(format_route(detour))
    if detour.found:
        diff = compare_routes(original, detour)
        print(f"  Detour costs +{diff['extra']:.1f} km ({diff['percent']:.1f}% longer)")
    print(f"  Road restored afterwards: {graph.has_road(*blocked[0])}")

    a, b = edges[0]
    slowed = apply_traffic(graph, {(a, b): 3.0})
    print(f"\n  Heavy traffic on {a} - {b} (x3):")
    print(format_route(dijkstra(slowed, START, GOAL)))
    return blocked, detour


# ----- 5. Visualization ----------------------------------------------------
def demo_visualization(graph: Graph, route: PathResult, blocked: list[tuple[str, str]],
                       detour: PathResult, rows: list[ComparisonRow], show: bool) -> None:
    section("5. Visualization with networkx + matplotlib  - Member 4")
    if not HAS_PLOTTING:
        print("  Skipped: install the plotting libraries with  pip install -r requirements.txt")
        return
    import matplotlib
    if not show:
        matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from study_case.member4_visualization import ALT_COLOR, draw_map, plot_performance, save_figure

    figures = {
        "1_map.png": draw_map(graph, title="Sample City map"),
        "2_shortest_route.png": draw_map(graph, route.path,
                                         title=f"Shortest route {START} → {GOAL}: {route.distance:.1f} km"),
        "3_blocked_route.png": draw_map(graph, detour.path, blocked=blocked, path_color=ALT_COLOR,
                                        title=f"Detour around blocked road: {detour.distance:.1f} km"),
        "4_performance.png": plot_performance(rows, title="Dijkstra vs A* on a 40x40 grid city"),
    }
    for filename, fig in figures.items():
        print(f"  saved {save_figure(fig, OUTPUT_DIR / filename).relative_to(ROOT)}")
    if show:
        plt.show()
    plt.close("all")


# ----- 6. Prototype --------------------------------------------------------
MENU = """
  1) List locations          4) Block a road
  2) Route with Dijkstra     5) Reopen all roads
  3) Route with A*           6) Show map
  0) Exit"""


def ask_location(graph: Graph, prompt: str) -> str | None:
    name = input(prompt).strip()
    match = {n.lower(): n for n in graph.locations}.get(name.lower())
    if match is None:
        print(f"  Unknown location '{name}'.")
    return match


def run_prototype(graph: Graph) -> None:
    section("Route Finder prototype")
    blocked: list[tuple[str, str]] = []
    last_path: list[str] = []
    while True:
        print(MENU)
        if blocked:
            print("  Blocked: " + ", ".join(f"{a}-{b}" for a, b in blocked))
        choice = input("  Choose: ").strip()
        if choice == "0":
            break
        if choice == "1":
            print("  " + ", ".join(graph.locations))
        elif choice in ("2", "3"):
            start = ask_location(graph, "  From: ")
            goal = start and ask_location(graph, "  To:   ")
            if goal:
                algorithm = dijkstra if choice == "2" else astar
                result = find_route_avoiding(graph, start, goal, blocked, algorithm)
                last_path = result.path
                print(format_route(result))
        elif choice == "4":
            a = ask_location(graph, "  Road from: ")
            b = a and ask_location(graph, "  Road to:   ")
            if b and graph.has_road(a, b) and (a, b) not in blocked and (b, a) not in blocked:
                blocked.append((a, b))
                print(f"  Road {a}-{b} blocked.")
            elif b:
                print("  No open road between those locations.")
        elif choice == "5":
            blocked.clear()
            print("  All roads reopened.")
        elif choice == "6":
            if not HAS_PLOTTING:
                print("  Install matplotlib and networkx to show the map.")
                continue
            import matplotlib.pyplot as plt
            from study_case.member4_visualization import draw_map
            draw_map(graph, last_path, blocked=blocked, title="Route Finder")
            plt.show()
        else:
            print("  Please choose a number from the menu.")


# ----- tests ---------------------------------------------------------------
def run_tests() -> bool:
    suite = unittest.defaultTestLoader.discover(str(ROOT / "test_case"), top_level_dir=str(ROOT))
    return unittest.TextTestRunner(verbosity=2).run(suite).wasSuccessful()


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Route Finder demonstration")
    parser.add_argument("--interactive", action="store_true", help="run the interactive prototype")
    parser.add_argument("--no-show", action="store_true", help="save graphs without opening windows")
    parser.add_argument("--test", action="store_true", help="run all test cases")
    args = parser.parse_args(argv)

    if args.test:
        return 0 if run_tests() else 1

    graph = load_sample_graph()
    if args.interactive:
        run_prototype(graph)
        return 0

    demo_graph(graph)
    route = demo_dijkstra(graph)
    _, rows = demo_astar(graph, route)
    blocked, detour = demo_road_blocking(graph, route)
    demo_visualization(graph, route, blocked, detour, rows, show=not args.no_show)
    print("\nDone. Try the prototype:  python demonstration/main.py --interactive")
    return 0


if __name__ == "__main__":
    sys.exit(main())
