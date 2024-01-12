use rust_quadtree::quadtree::{Point, QuadTree, Rectangle, Size};

#[test]
fn test_quadtree_insertion() {
    // Define the boundary of the whole quadtree
    let boundary = Rectangle {
        top_left: Point { x: 0.0, y: 0.0 },
        size: Size {
            width: 1.0,
            height: 1.0,
        },
    };

    // Create a new QuadTree
    let mut qt = QuadTree::new(boundary);

    // Insert some items into the QuadTree
    qt.insert(Rectangle {
        top_left: Point { x: 0.1, y: 0.1 },
        size: Size {
            width: 0.1,
            height: 0.1,
        },
    });
    qt.insert(Rectangle {
        top_left: Point { x: 0.2, y: 0.2 },
        size: Size {
            width: 0.1,
            height: 0.1,
        },
    });

    // Query a point
    let query_point = Point { x: 0.15, y: 0.15 };
    let found_ids = qt.query_point(&query_point);

    // Print the found IDs
    println!("Found IDs: {:?}", found_ids);

    // Query a point
    let query_point = Point { x: 0.25, y: 0.25 };
    let found_ids = qt.query_point(&query_point);

    // Print the found IDs
    println!("Found IDs: {:?}", found_ids);
}
