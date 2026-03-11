use crate::quadtree::{Point, QuadTree, Rectangle, Size};

mod quadtree;

fn main() {
    let mut qt = QuadTree::new(Rectangle {
        top_left: Point { x: 0.0, y: 0.0 },
        size: Size {
            width: 1.0,
            height: 1.0,
        },
    });

    // get time for performance measurement

    // insert 1000 rectangles
    let num_rects = 1_000;
    let rect_size = 1.0 / num_rects as f32;

    // let rects = (0..num_rects)
    //     .map(|i| {
    //         let x = i as f32 * rect_size;
    //         let y = i as f32 * rect_size;
    //         vec![x, y, rect_size, rect_size]
    //     })
    //     .flatten()
    //     .collect::<Vec<_>>();

    // lets try random positions and sizes, less than 1.0
    let mut rects = vec![];
    let rect_size = 1.0;
    for _ in 0..num_rects {
        let x = rand::random::<f32>();
        let y = rand::random::<f32>();
        let w = rect_size;
        let h = rect_size;
        rects.push(x);
        rects.push(y);
        rects.push(w);
        rects.push(h);
    }

    let start = std::time::Instant::now();
    qt.insert_many(&rects);
    let elapsed = start.elapsed();

    println!(
        "inserted {} rectangles in {:.6} ms",
        num_rects,
        elapsed.as_nanos() as f64 / 1_000_000.0
    );
}
