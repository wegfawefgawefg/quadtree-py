# Improvement Ideas

This repo is already in a decent archival state, but there are a few obvious directions if it ever gets revisited.

## Performance

- Avoid allocating a fresh `Vec` for every Rust point query.
  - The current API still allocates query result storage on each call.
  - A reusable output buffer or callback-style interface could reduce overhead.
- Add a true bulk-build path.
  - Right now both implementations are built through repeated inserts.
  - A construction path from a full rectangle set could be faster and more consistent.
- Benchmark larger and more varied workloads.
  - Dense overlap cases
  - Sparse cases
  - Skewed spatial distributions
  - Tiny vs large rectangles
- Keep comparing single-query versus batched-query FFI.
  - The current `query_many_points` path already shows that reducing Python<->Rust boundary crossings helps.
- Add a pure Rust benchmark.
  - That would separate actual quadtree speed from Python/`ctypes` overhead.

## API / Packaging

- Package the Rust-backed quadtree more cleanly for Python users.
  - Right now this is still a local experiment layout.
  - A real package could build or bundle the Rust library so Python users can `pip install` and import it directly.
- Consider a more robust Python/Rust bridge if the project ever becomes serious.
  - `ctypes` is fine for a quick experiment.
  - A packaging-oriented bridge such as `pyo3`/`maturin` would likely be a better long-term fit.
- Make the import path feel less experimental.
  - The local package works now, but a polished version would expose a cleaner top-level Python API.

## Correctness / Productization

- Add more query types:
  - rectangle query
  - overlap query
  - delete/update operations
- Add more consistency tests between the Python and Rust implementations.
- Document the quadtree behavior for rectangles spanning multiple child nodes.
  - That was one of the major correctness pitfalls in the original experiment.

## Bottom Line

If this ever comes back from archive status, the most valuable next step is probably:

1. benchmark and optimize the Rust core more carefully
2. package it like a real Python-importable library
3. expand the query/update API beyond point queries
