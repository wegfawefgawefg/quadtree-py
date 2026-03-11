from __future__ import annotations

import ctypes
import subprocess
import sys
from pathlib import Path


def _repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


def _library_candidates() -> list[Path]:
    release_dir = _repo_root() / "rust_quadtree" / "target" / "release"
    if sys.platform == "win32":
        return [release_dir / "quadtree.dll", release_dir / "libquadtree.dll"]
    if sys.platform == "darwin":
        return [release_dir / "libquadtree.dylib"]
    return [release_dir / "libquadtree.so"]


def build_release() -> None:
    subprocess.run(
        ["cargo", "build", "--release"],
        cwd=_repo_root() / "rust_quadtree",
        check=True,
    )


def _load_library(build_if_missing: bool) -> ctypes.CDLL:
    for candidate in _library_candidates():
        if candidate.exists():
            return ctypes.CDLL(str(candidate))

    if build_if_missing:
        build_release()
        for candidate in _library_candidates():
            if candidate.exists():
                return ctypes.CDLL(str(candidate))

    candidates = ", ".join(str(path) for path in _library_candidates())
    raise FileNotFoundError(
        f"Could not find compiled rust_quadtree library. Looked for: {candidates}"
    )


class RustQuadTree:
    def __init__(
        self, x: float, y: float, width: float, height: float, *, build_if_missing: bool = False
    ):
        self.lib = _load_library(build_if_missing)

        self.lib.quadtree_new.argtypes = [
            ctypes.c_float,
            ctypes.c_float,
            ctypes.c_float,
            ctypes.c_float,
        ]
        self.lib.quadtree_new.restype = ctypes.c_void_p

        self.lib.quadtree_insert_many.argtypes = [
            ctypes.c_void_p,
            ctypes.POINTER(ctypes.c_float),
            ctypes.c_size_t,
        ]
        self.lib.quadtree_insert_many.restype = None

        self.lib.quadtree_query_point.argtypes = [
            ctypes.c_void_p,
            ctypes.c_float,
            ctypes.c_float,
            ctypes.POINTER(ctypes.c_size_t),
        ]
        self.lib.quadtree_query_point.restype = ctypes.POINTER(ctypes.c_uint)

        self.lib.quadtree_query_results_free.argtypes = [
            ctypes.POINTER(ctypes.c_uint),
            ctypes.c_size_t,
        ]
        self.lib.quadtree_query_results_free.restype = None

        self.lib.quadtree_free.argtypes = [ctypes.c_void_p]
        self.lib.quadtree_free.restype = None

        self.tree = self.lib.quadtree_new(x, y, width, height)

    def insert_many(self, rects: list[float]) -> None:
        flat_rects = (ctypes.c_float * len(rects))(*rects)
        self.lib.quadtree_insert_many(self.tree, flat_rects, len(rects))

    def query_point(self, x: float, y: float) -> list[int]:
        length = ctypes.c_size_t()
        ids_ptr = self.lib.quadtree_query_point(self.tree, x, y, ctypes.byref(length))
        if not ids_ptr:
            return []

        try:
            return [int(ids_ptr[i]) for i in range(length.value)]
        finally:
            self.lib.quadtree_query_results_free(ids_ptr, length.value)

    def close(self) -> None:
        if getattr(self, "tree", None):
            self.lib.quadtree_free(self.tree)
            self.tree = None

    def __del__(self) -> None:
        self.close()
