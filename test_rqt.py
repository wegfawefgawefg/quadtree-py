import time
import unittest

from rqt import QuadTree


class TestFFIQuadTree(unittest.TestCase):
    def setUp(self):
        pass

    def test_query(self):
        quadtree = QuadTree(0.0, 0.0, 1.0, 1.0)
        quadtree.insert_many([0.0, 0.0, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5])
        ids = quadtree.query_point(0.25, 0.25)
        first_id = ids[0]
        self.assertEqual(first_id, 0)
        ids = quadtree.query_point(0.75, 0.75)
        first_id = ids[0]
        self.assertEqual(first_id, 1)

    def test_init_speed(self):
        ms_max = 1

        start_time = time.perf_counter()  # Start time
        QuadTree(0.0, 0.0, 1.0, 1.0)
        end_time = time.perf_counter()  # End time

        execution_time = (end_time - start_time) * 1000  # Convert to milliseconds
        self.assertLess(execution_time, ms_max, "Init took longer than 3 milliseconds")

    def test_query_accuracy(self):
        num_rects = 10
        qt = QuadTree(0.0, 0.0, 1.0, 1.0)
        rects = []
        for i in range(num_rects):
            x = 0.0
            y = 0.0
            w = 1.0
            h = 1.0
            rects.append(x)
            rects.append(y)
            rects.append(w)
            rects.append(h)
        qt.insert_many(rects)

        ids = qt.query_point(0.75, 0.75)

        # assert ids has 10 elements
        self.assertEqual(len(ids), num_rects)

    def test_build_speed(self):
        num_rects = 1_000
        ms_max = 1.0

        qt = QuadTree(0.0, 0.0, 1.0, 1.0)
        rects = []
        for i in range(num_rects):
            x = i / 1000
            y = i / 1000
            w = 1.0
            h = 1.0
            rects.append(x)
            rects.append(y)
            rects.append(w)
            rects.append(h)

        start_time = time.perf_counter()  # Start time
        qt.insert_many(rects)
        end_time = time.perf_counter()  # End time

        execution_time = (end_time - start_time) * 1000  # Convert to milliseconds
        self.assertLess(
            execution_time,
            ms_max,
            f"Insertions took too long",
        )

    def test_query_speed(self):
        num_rects = 1_000
        num_queries = 100
        ms_max = 1.0

        qt = QuadTree(0.0, 0.0, 1.0, 1.0)
        rects = []
        for i in range(num_rects):
            x = i / 1000
            y = i / 1000
            w = 0.2
            h = 0.2
            rects.extend([x, y, w, h])

        qt.insert_many(rects)

        # query
        start_time = time.perf_counter()  # Start time
        for i in range(num_queries):
            ids = qt.query_point(i / num_queries, i / num_queries)
        end_time = time.perf_counter()  # End time

        execution_time = (end_time - start_time) * 1000  # Convert to milliseconds
        self.assertLess(
            execution_time,
            ms_max,
            f"{num_queries} queries took too long",
        )


# Run the tests
if __name__ == "__main__":
    unittest.main()
