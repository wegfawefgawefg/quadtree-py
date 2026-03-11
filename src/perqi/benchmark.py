from __future__ import annotations

import argparse
import random
import statistics
import time

from .native_quadtree import QuadTreeNode, Rectangle
from .rust_quadtree import RustQuadTree


def make_rects(num_rects: int, seed: int) -> list[tuple[float, float, float, float]]:
    rng = random.Random(seed)
    rects: list[tuple[float, float, float, float]] = []
    for _ in range(num_rects):
        width = rng.uniform(0.01, 0.08)
        height = rng.uniform(0.01, 0.08)
        x = rng.uniform(0.0, 1.0 - width)
        y = rng.uniform(0.0, 1.0 - height)
        rects.append((x, y, width, height))
    return rects


def make_queries(num_queries: int, seed: int) -> list[tuple[float, float]]:
    rng = random.Random(seed)
    return [(rng.random(), rng.random()) for _ in range(num_queries)]


def build_native(rects: list[tuple[float, float, float, float]]) -> QuadTreeNode[int]:
    tree = QuadTreeNode(Rectangle(0.0, 0.0, 1.0, 1.0))
    for idx, (x, y, w, h) in enumerate(rects):
        tree.insert(Rectangle(x, y, w, h, idx))
    return tree


def build_rust(rects: list[tuple[float, float, float, float]], *, build_if_missing: bool) -> RustQuadTree:
    tree = RustQuadTree(0.0, 0.0, 1.0, 1.0, build_if_missing=build_if_missing)
    flat: list[float] = []
    for x, y, w, h in rects:
        flat.extend((x, y, w, h))
    tree.insert_many(flat)
    return tree


def native_query(tree: QuadTreeNode[int], queries: list[tuple[float, float]]) -> list[list[int]]:
    results: list[list[int]] = []
    for x, y in queries:
        found: list[int] = []
        tree.query(x, y, found)
        results.append(sorted(found))
    return results


def rust_query(tree: RustQuadTree, queries: list[tuple[float, float]]) -> list[list[int]]:
    results: list[list[int]] = []
    for x, y in queries:
        results.append(sorted(tree.query_point(x, y)))
    return results


def benchmark(name: str, fn, repeats: int) -> tuple[float, float]:
    samples: list[float] = []
    for _ in range(repeats):
        start = time.perf_counter()
        fn()
        end = time.perf_counter()
        samples.append((end - start) * 1000.0)
    return statistics.mean(samples), min(samples)


def main() -> None:
    parser = argparse.ArgumentParser(description="Headless quadtree benchmark")
    parser.add_argument("--rects", type=int, default=10_000)
    parser.add_argument("--queries", type=int, default=2_000)
    parser.add_argument("--repeats", type=int, default=5)
    parser.add_argument("--seed", type=int, default=1234)
    parser.add_argument("--build-rust", action="store_true")
    args = parser.parse_args()

    rects = make_rects(args.rects, args.seed)
    queries = make_queries(args.queries, args.seed + 1)

    native_build_ms, native_build_best = benchmark(
        "native-build", lambda: build_native(rects), args.repeats
    )
    native_tree = build_native(rects)
    native_query_ms, native_query_best = benchmark(
        "native-query", lambda: native_query(native_tree, queries), args.repeats
    )

    rust_build_ms, rust_build_best = benchmark(
        "rust-build", lambda: build_rust(rects, build_if_missing=args.build_rust).close(), args.repeats
    )
    rust_tree = build_rust(rects, build_if_missing=args.build_rust)
    rust_query_ms, rust_query_best = benchmark(
        "rust-query", lambda: rust_query(rust_tree, queries), args.repeats
    )

    native_results = native_query(native_tree, queries[:100])
    rust_results = rust_query(rust_tree, queries[:100])
    rust_tree.close()
    if native_results != rust_results:
        raise SystemExit("native and rust query results diverged")

    print(f"rectangles: {args.rects}")
    print(f"queries: {args.queries}")
    print()
    print(f"native build: mean {native_build_ms:.3f} ms | best {native_build_best:.3f} ms")
    print(f"native query: mean {native_query_ms:.3f} ms | best {native_query_best:.3f} ms")
    print(f"rust build:   mean {rust_build_ms:.3f} ms | best {rust_build_best:.3f} ms")
    print(f"rust query:   mean {rust_query_ms:.3f} ms | best {rust_query_best:.3f} ms")
