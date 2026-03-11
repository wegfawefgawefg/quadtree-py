import unittest

from perqi.native_quadtree import QuadTreeNode, Rectangle


class NativeQuadTreeTests(unittest.TestCase):
    def test_query_simple_hit(self) -> None:
        tree = QuadTreeNode(Rectangle(0.0, 0.0, 1.0, 1.0))
        tree.insert(Rectangle(0.1, 0.1, 0.2, 0.2, "r1"))
        tree.insert(Rectangle(0.3, 0.3, 0.2, 0.2, "r2"))

        found: list[str] = []
        tree.query(0.15, 0.15, found)

        self.assertIn("r1", found)
        self.assertNotIn("r2", found)

    def test_spanning_rect_stays_queryable(self) -> None:
        tree = QuadTreeNode(Rectangle(0.0, 0.0, 1.0, 1.0))
        for idx in range(4):
            tree.insert(Rectangle(idx * 0.1, idx * 0.1, 0.05, 0.05, idx))

        spanning = Rectangle(0.45, 0.45, 0.2, 0.2, "spanning")
        tree.insert(spanning)

        found: list[str] = []
        tree.query(0.6, 0.6, found)

        self.assertIn("spanning", found)


if __name__ == "__main__":
    unittest.main()
