from rqt import QuadTree

quadtree = QuadTree(0.0, 0.0, 100.0, 100.0)

# Insert rectangles
quadtree.insert_many([0.0, 0.0, 10.0, 10.0, 20.0, 20.0, 5.0, 5.0])

# # Query a point
ids = quadtree.query_point(5.0, 5.0)
print(ids)

ids = quadtree.query_point(21.0, 21.0)
print(ids)
print(type(ids[0]))
