from __future__ import annotations

from dataclasses import dataclass
from typing import Generic, TypeVar

T = TypeVar("T")


@dataclass(slots=True)
class Rectangle(Generic[T]):
    x: float
    y: float
    width: float
    height: float
    data: T | None = None

    @property
    def right(self) -> float:
        return self.x + self.width

    @property
    def bottom(self) -> float:
        return self.y + self.height

    def contains_point(self, px: float, py: float) -> bool:
        return self.x <= px <= self.right and self.y <= py <= self.bottom

    def contains_rect(self, other: "Rectangle[object]") -> bool:
        return (
            self.x <= other.x
            and self.y <= other.y
            and self.right >= other.right
            and self.bottom >= other.bottom
        )

    def intersects(self, other: "Rectangle[object]") -> bool:
        return (
            self.x < other.right
            and self.right > other.x
            and self.y < other.bottom
            and self.bottom > other.y
        )


class QuadTreeNode(Generic[T]):
    MAX_ITEMS = 4

    def __init__(self, boundary: Rectangle[object]):
        self.boundary = boundary
        self.rectangles: list[Rectangle[T]] = []
        self.children: list[QuadTreeNode[T] | None] = [None, None, None, None]

    def subdivide(self) -> None:
        half_w = self.boundary.width / 2.0
        half_h = self.boundary.height / 2.0
        x = self.boundary.x
        y = self.boundary.y
        self.children = [
            QuadTreeNode(Rectangle(x, y, half_w, half_h)),
            QuadTreeNode(Rectangle(x + half_w, y, half_w, half_h)),
            QuadTreeNode(Rectangle(x, y + half_h, half_w, half_h)),
            QuadTreeNode(Rectangle(x + half_w, y + half_h, half_w, half_h)),
        ]

    def _child_that_fully_contains(
        self, rectangle: Rectangle[T]
    ) -> QuadTreeNode[T] | None:
        for child in self.children:
            if child is not None and child.boundary.contains_rect(rectangle):
                return child
        return None

    def insert(self, rectangle: Rectangle[T]) -> bool:
        if not self.boundary.intersects(rectangle):
            return False

        if self.children[0] is not None:
            child = self._child_that_fully_contains(rectangle)
            if child is not None:
                return child.insert(rectangle)

        if len(self.rectangles) < self.MAX_ITEMS:
            self.rectangles.append(rectangle)
            return True

        if self.children[0] is None:
            self.subdivide()

        child = self._child_that_fully_contains(rectangle)
        if child is not None:
            return child.insert(rectangle)

        # Spanning rectangles stay at the current node.
        self.rectangles.append(rectangle)
        return True

    def query(self, px: float, py: float, found: list[T]) -> None:
        if not self.boundary.contains_point(px, py):
            return

        for rectangle in self.rectangles:
            if rectangle.contains_point(px, py):
                found.append(rectangle.data)  # type: ignore[arg-type]

        for child in self.children:
            if child is not None:
                child.query(px, py, found)
