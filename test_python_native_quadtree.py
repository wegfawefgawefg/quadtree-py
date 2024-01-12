import time
import unittest

import glm

from quadtree import Rectangle, QuadTreeNode


class TestQuadTreeNode(unittest.TestCase):
    def setUp(self):
        self.root = QuadTreeNode(Rectangle(glm.vec2(0, 0), glm.vec2(1.0, 1.0), None))
        self.r1 = Rectangle(glm.vec2(0.1, 0.1), glm.vec2(0.2, 0.2), "r1")
        self.r2 = Rectangle(glm.vec2(0.3, 0.3), glm.vec2(0.2, 0.2), "r2")
        self.root.insert(self.r1)
        self.root.insert(self.r2)

    def test_insert(self):
        self.assertIn(self.r1, self.root.rectangles)
        self.assertIn(self.r2, self.root.rectangles)

    def test_query(self):
        found_data = []
        self.root.query(glm.vec2(0.15, 0.15), found_data)
        self.assertIn("r1", found_data)
        self.assertNotIn("r2", found_data)

    def test_insert_speed(self):
        test_rectangle = Rectangle(glm.vec2(0.4, 0.4), glm.vec2(0.2, 0.2), "r3")

        start_time = time.perf_counter()  # Start time
        self.root.insert(test_rectangle)
        end_time = time.perf_counter()  # End time

        execution_time = (end_time - start_time) * 1000  # Convert to milliseconds
        self.assertLess(
            execution_time, 10, "Insert method took longer than 10 milliseconds"
        )

    # lets fill it with a huge number of rectangles, and make many queries
    def test_build_speed(self):
        num_rects = 200
        ms_max = 3

        # populate quadtree
        start_time = time.perf_counter()  # Start time
        for i in range(num_rects):
            self.root.insert(
                Rectangle(
                    glm.vec2(i / 1000, i / 1000), glm.vec2(0.2, 0.2), "r" + str(i)
                )
            )
        end_time = time.perf_counter()  # End time

        execution_time = (end_time - start_time) * 1000  # Convert to milliseconds
        self.assertLess(
            execution_time,
            ms_max,
            f"Insertions took too long",
        )

    def test_query_speed(self):
        num_rects = 1000
        num_queries = 5
        ms_max = 0.3

        # make rectangles
        for i in range(num_rects):
            self.root.insert(
                Rectangle(
                    glm.vec2(i / 1000, i / 1000), glm.vec2(0.2, 0.2), "r" + str(i)
                )
            )

        # query
        start_time = time.perf_counter()  # Start time
        for i in range(num_queries):
            found_data = []
            self.root.query(glm.vec2(i / 1000, i / 1000), found_data)
            self.assertIn("r" + str(i), found_data)
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
