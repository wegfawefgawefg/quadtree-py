import glm


class Rectangle:
    def __init__(self, position, size, data):
        self.position = position
        self.size = size
        self.data = data

    def contains(self, point):
        return (
            self.position.x <= point.x < self.position.x + self.size.x
            and self.position.y <= point.y < self.position.y + self.size.y
        )


class QuadTreeNode:
    def __init__(self, boundary):
        self.boundary = boundary  # rectangle
        self.rectangles = []  # quads
        self.children = [None] * 4  # quads

    def subdivide(self):
        # Subdivide the current quad into four quads
        x, y = self.boundary.position.x, self.boundary.position.y
        w, h = self.boundary.size.x / 2, self.boundary.size.y / 2
        self.children[0] = QuadTreeNode(Rectangle(glm.vec2(x, y), glm.vec2(w, h), None))
        self.children[1] = QuadTreeNode(
            Rectangle(glm.vec2(x + w, y), glm.vec2(w, h), None)
        )
        self.children[2] = QuadTreeNode(
            Rectangle(glm.vec2(x, y + h), glm.vec2(w, h), None)
        )
        self.children[3] = QuadTreeNode(
            Rectangle(glm.vec2(x + w, y + h), glm.vec2(w, h), None)
        )

    def insert(self, rectangle):
        # Check if the rectangle can be inserted in this quad
        if not self.boundary.contains(
            glm.vec2(rectangle.position.x, rectangle.position.y)
        ):
            return False

        # If there's space in this quad and no subdivisions, add the rectangle here
        if len(self.rectangles) < 4 and not self.children[0]:
            self.rectangles.append(rectangle)
            return True

        # Subdivide if necessary
        if not self.children[0]:
            self.subdivide()

        # Insert the rectangle into the appropriate quadrant
        for child in self.children:
            if child.insert(rectangle):
                return True

        # If unable to insert the rectangle (shouldn't happen if the code is correct)
        return False

    def query(self, point, found):
        # Ignore if point is not within boundary
        if not self.boundary.contains(point):
            return

        # Check each rectangle in this quad
        for rectangle in self.rectangles:
            if rectangle.contains(point):
                found.append(rectangle.data)

        # If there are no children, return
        if not self.children[0]:
            return

        # Otherwise, continue querying in the relevant quads
        for child in self.children:
            child.query(point, found)


# # Example Usage
# root = QuadTreeNode(Rectangle(glm.vec2(0, 0), glm.vec2(1.0, 1.0), None))

# # Insert rectangles
# r1 = Rectangle(glm.vec2(0.1, 0.1), glm.vec2(0.2, 0.2), "r1")
# r2 = Rectangle(glm.vec2(0.3, 0.3), glm.vec2(0.2, 0.2), "r2")
# root.insert(r1)
# root.insert(r2)

# # Query
# found_data = []
# p = glm.vec2(0.15, 0.15)
# root.query(p, found_data)
# print(found_data)
