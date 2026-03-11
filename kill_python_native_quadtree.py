import time
import unittest

import glm

from quadtree import Rectangle, QuadTreeNode


num_rects = 1000

# make rectangles

rect_size = 0.0
num_trials = 10
for i in range(num_trials):
    rect_size += 0.1
    qt = QuadTreeNode(Rectangle(glm.vec2(0, 0), glm.vec2(1.0, 1.0), 0))
    start_time = time.perf_counter()  # Start time
    for i in range(num_rects):
        r = Rectangle(glm.vec2(0.0, 0.0), glm.vec2(rect_size, rect_size), 0)
        qt.insert(r)
    end_time = time.perf_counter()  # End time
    execution_time = (end_time - start_time) * 1000  # Convert to milliseconds
    print(f"size: {rect_size}, {execution_time} millis")

# # query
# for i in range(num_queries):
#     found_data = []
#     self.root.query(glm.vec2(i / 1000, i / 1000), found_data)
#     self.assertIn("r" + str(i), found_data)
