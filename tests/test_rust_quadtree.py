import unittest

from perqi.rust_quadtree import RustQuadTree


class RustQuadTreeTests(unittest.TestCase):
    def test_query_simple_hit(self) -> None:
        tree = RustQuadTree(0.0, 0.0, 1.0, 1.0)
        try:
            tree.insert_many([0.0, 0.0, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5])
            self.assertEqual(tree.query_point(0.25, 0.25)[0], 0)
            self.assertEqual(tree.query_point(0.75, 0.75)[0], 1)
        finally:
            tree.close()

    def test_spanning_rect_stays_queryable(self) -> None:
        tree = RustQuadTree(0.0, 0.0, 1.0, 1.0)
        try:
            flat = []
            for idx in range(4):
                flat.extend((idx * 0.1, idx * 0.1, 0.05, 0.05))
            flat.extend((0.45, 0.45, 0.2, 0.2))
            tree.insert_many(flat)

            ids = tree.query_point(0.6, 0.6)
            self.assertIn(4, ids)
        finally:
            tree.close()


if __name__ == "__main__":
    unittest.main()
