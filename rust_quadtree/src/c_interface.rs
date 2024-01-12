use std::os::raw::{c_float, c_uint};

use crate::quadtree::{Point, QuadTree, Rectangle, Size};

#[no_mangle]
pub extern "C" fn quadtree_new(
    x: c_float,
    y: c_float,
    width: c_float,
    height: c_float,
) -> *mut QuadTree {
    let boundary = Rectangle {
        top_left: Point { x, y },
        size: Size { width, height },
    };
    Box::into_raw(Box::new(QuadTree::new(boundary)))
}

#[no_mangle]
#[allow(clippy::missing_safety_doc)]
pub unsafe extern "C" fn quadtree_insert_many(
    tree: *mut QuadTree,
    rects: *const c_float,
    count: usize,
) {
    if !tree.is_null() && !rects.is_null() {
        let tree = unsafe { &mut *tree };
        let rects = unsafe { std::slice::from_raw_parts(rects, count) };
        tree.insert_many(rects);
    }
}

// #[no_mangle]
// #[allow(clippy::missing_safety_doc)]
// pub unsafe extern "C" fn quadtree_query_point(
//     tree: *const QuadTree,
//     x: c_float,
//     y: c_float,
// ) -> *const c_uint {
//     let point = Point { x, y };
//     let ids = unsafe { (*tree).query_point(&point) };
//     let boxed_ids = Box::new(ids);
//     Box::into_raw(boxed_ids) as *const c_uint
// }

#[no_mangle]
#[allow(clippy::missing_safety_doc)]
pub unsafe extern "C" fn quadtree_query_point(
    tree: *const QuadTree,
    x: c_float,
    y: c_float,
    out_len: *mut usize,
) -> *mut i32 {
    if tree.is_null() || out_len.is_null() {
        return std::ptr::null_mut();
    }

    let tree = unsafe { &*tree };
    let point = Point { x, y };
    let ids = tree.query_point(&point);
    let len = ids.len();
    let boxed_ids = ids.into_boxed_slice();

    unsafe {
        *out_len = len;
    }

    Box::into_raw(boxed_ids) as *mut i32
}

#[no_mangle]
#[allow(clippy::missing_safety_doc)]
pub unsafe extern "C" fn quadtree_free(tree: *mut QuadTree) {
    if !tree.is_null() {
        unsafe {
            let _ = Box::from_raw(tree);
        };
    }
}
