pub struct Point {
    pub x: f32,
    pub y: f32,
}

pub struct Size {
    pub width: f32,
    pub height: f32,
}

pub struct Rectangle {
    pub top_left: Point,
    pub size: Size,
}

pub struct Item {
    pub area: Rectangle,
    pub id: u32,
}

impl Rectangle {
    pub fn contains(&self, point: &Point) -> bool {
        point.x >= self.top_left.x
            && point.x <= self.top_left.x + self.size.width
            && point.y >= self.top_left.y
            && point.y <= self.top_left.y + self.size.height
    }

    pub fn intersects(&self, other: &Rectangle) -> bool {
        self.top_left.x < other.top_left.x + other.size.width
            && self.top_left.x + self.size.width > other.top_left.x
            && self.top_left.y < other.top_left.y + other.size.height
            && self.top_left.y + self.size.height > other.top_left.y
    }
}

pub struct QuadTree {
    next_id: u32,
    root: QuadTreeNode,
}

impl QuadTree {
    pub fn new(boundary: Rectangle) -> QuadTree {
        QuadTree {
            next_id: 0,
            root: QuadTreeNode::new(boundary),
        }
    }

    pub fn insert_many(&mut self, rects: &[f32]) {
        for chunk in rects.chunks(4) {
            if chunk.len() == 4 {
                let rect = Rectangle {
                    top_left: Point {
                        x: chunk[0],
                        y: chunk[1],
                    },
                    size: Size {
                        width: chunk[2],
                        height: chunk[3],
                    },
                };
                self.insert(rect);
            }
        }
    }

    pub fn insert(&mut self, rect: Rectangle) {
        self.root.insert(&rect, self.next_id);
        self.next_id += 1;
    }

    pub fn query_point(&self, point: &Point) -> Vec<u32> {
        self.root.query_point(point)
    }
}

struct QuadTreeNode {
    boundary: Rectangle,
    items: Vec<Item>,
    children: Option<Box<[QuadTreeNode; 4]>>,
}

impl QuadTreeNode {
    const MAX_ITEMS: usize = 4;

    pub fn new(boundary: Rectangle) -> QuadTreeNode {
        QuadTreeNode {
            boundary,
            items: Vec::new(),
            children: None,
        }
    }

    pub fn insert(&mut self, rect: &Rectangle, id: u32) {
        // If the rectangle does not intersect with this node's boundary, do nothing
        if !self.boundary.intersects(rect) {
            return;
        }

        // If the current node has space for more items, just add the item
        if self.items.len() < QuadTreeNode::MAX_ITEMS && self.children.is_none() {
            self.items.push(Item {
                area: Rectangle {
                    top_left: Point {
                        x: rect.top_left.x,
                        y: rect.top_left.y,
                    },
                    size: Size {
                        width: rect.size.width,
                        height: rect.size.height,
                    },
                },
                id,
            });
        } else {
            // If the node is already full, subdivide it if it hasn't been subdivided yet
            if self.children.is_none() {
                self.subdivide();
            }

            // Try to insert the item into each of the children
            if let Some(ref mut children) = self.children {
                for child in children.iter_mut() {
                    child.insert(rect, id);
                }
            }
        }
    }

    pub fn query_point(&self, point: &Point) -> Vec<u32> {
        let mut found_items = Vec::new();

        // Check if the point is outside the bounds of this node
        if !self.boundary.contains(point) {
            return found_items;
        }

        // Check each item in the current node
        for item in &self.items {
            if item.area.contains(point) {
                found_items.push(item.id);
            }
        }

        // If the node has children, recursively query them
        if let Some(ref children) = self.children {
            for child in children.iter() {
                found_items.extend(child.query_point(point));
            }
        }

        found_items
    }

    fn subdivide(&mut self) {
        let width = self.boundary.size.width / 2.0;
        let height = self.boundary.size.height / 2.0;

        let x = self.boundary.top_left.x;
        let y = self.boundary.top_left.y;

        let children = Box::new([
            QuadTreeNode::new(Rectangle {
                top_left: Point { x, y },
                size: Size { width, height },
            }),
            QuadTreeNode::new(Rectangle {
                top_left: Point { x: x + width, y },
                size: Size { width, height },
            }),
            QuadTreeNode::new(Rectangle {
                top_left: Point { x, y: y + height },
                size: Size { width, height },
            }),
            QuadTreeNode::new(Rectangle {
                top_left: Point {
                    x: x + width,
                    y: y + height,
                },
                size: Size { width, height },
            }),
        ]);

        self.children = Some(children);
    }
}
