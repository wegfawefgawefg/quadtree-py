pub mod c_interface;
pub mod quadtree;

pub use crate::c_interface::{
    quadtree_free, quadtree_insert_many, quadtree_new, quadtree_query_point,
    quadtree_query_results_free,
};
pub use crate::quadtree::{Point, QuadTree, Rectangle, Size};
