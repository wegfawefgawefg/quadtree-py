use std::os::raw::{c_float, c_uint};

use crate::quadtree::{Point, QuadTree, Rectangle, Size};

#[repr(C)]
pub struct QueryManyResult {
    ids: *mut c_uint,
    ids_len: usize,
    counts: *mut usize,
    counts_len: usize,
}

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

#[no_mangle]
#[allow(clippy::missing_safety_doc)]
pub unsafe extern "C" fn quadtree_query_point(
    tree: *const QuadTree,
    x: c_float,
    y: c_float,
    out_len: *mut usize,
) -> *mut c_uint {
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

    Box::into_raw(boxed_ids) as *mut c_uint
}

#[no_mangle]
#[allow(clippy::missing_safety_doc)]
pub unsafe extern "C" fn quadtree_query_many_points(
    tree: *const QuadTree,
    points: *const c_float,
    count: usize,
) -> QueryManyResult {
    if tree.is_null() || points.is_null() {
        return QueryManyResult {
            ids: std::ptr::null_mut(),
            ids_len: 0,
            counts: std::ptr::null_mut(),
            counts_len: 0,
        };
    }

    let tree = unsafe { &*tree };
    let points = unsafe { std::slice::from_raw_parts(points, count) };
    let (ids, counts) = tree.query_many_points(points);

    let ids_len = ids.len();
    let counts_len = counts.len();
    let ids = Box::into_raw(ids.into_boxed_slice()) as *mut c_uint;
    let counts = Box::into_raw(counts.into_boxed_slice()) as *mut usize;

    QueryManyResult {
        ids,
        ids_len,
        counts,
        counts_len,
    }
}

#[no_mangle]
#[allow(clippy::missing_safety_doc)]
pub unsafe extern "C" fn quadtree_query_results_free(ids: *mut c_uint, len: usize) {
    if !ids.is_null() {
        unsafe {
            let _ = Vec::from_raw_parts(ids, len, len);
        };
    }
}

#[no_mangle]
#[allow(clippy::missing_safety_doc)]
pub unsafe extern "C" fn quadtree_query_many_results_free(result: QueryManyResult) {
    if !result.ids.is_null() {
        unsafe {
            let _ = Vec::from_raw_parts(result.ids, result.ids_len, result.ids_len);
        };
    }
    if !result.counts.is_null() {
        unsafe {
            let _ = Vec::from_raw_parts(result.counts, result.counts_len, result.counts_len);
        };
    }
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
