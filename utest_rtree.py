import random
import time
from rtree import index


# Function to create an R-tree index
def create_rtree():
    p = index.Property()
    p.dimension = 2  # We are working in 2D space
    idx = index.Index(properties=p)
    return idx


def point_query(idx, point):
    return list(idx.intersection(point, objects="raw"))


def is_point_in_rect(point, rect):
    return (
        point[0] >= rect[0]
        and point[0] <= rect[2]
        and point[1] >= rect[1]
        and point[1] <= rect[3]
    )


# Example usage
rt = create_rtree()
control = []
for i in range(5000):
    # rt.insert(i, (0, 0, 10, 10))
    #  random rectangles
    x = random.random()
    y = random.random()
    w = random.random()
    h = random.random()
    rt.insert(i, (x, y, x + w, y + h))
    control.append((x, y, x + w, y + h))


# tree query time
start_time = time.perf_counter()  # Start time
num_queries = 1
for i in range(num_queries):
    ids = point_query(rt, (i / num_queries, i / num_queries))
end_time = time.perf_counter()  # End time

execution_time = (end_time - start_time) * 1000  # Convert to milliseconds
print(f"tree: {num_queries} queries took {execution_time} ms")

# control query time
start_time = time.perf_counter()  # Start time
num_queries = 1
for i in range(num_queries):
    ids = []
    for j in range(len(control)):
        if is_point_in_rect((i / num_queries, i / num_queries), control[j]):
            ids.append(j)
end_time = time.perf_counter()  # End time

execution_time = (end_time - start_time) * 1000  # Convert to milliseconds
print(f"control: {num_queries} queries took {execution_time} ms")
