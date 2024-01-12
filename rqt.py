import ctypes


class QuadTree:
    def __init__(self, x, y, width, height):
        self.lib = ctypes.CDLL("./rust_quadtree/target/release/libquadtree.so")

        self.lib.quadtree_new.argtypes = [
            ctypes.c_float,
            ctypes.c_float,
            ctypes.c_float,
            ctypes.c_float,
        ]
        self.lib.quadtree_new.restype = ctypes.c_void_p

        self.lib.quadtree_insert_many.argtypes = [
            ctypes.c_void_p,
            ctypes.POINTER(ctypes.c_float),
            ctypes.c_size_t,
        ]
        self.lib.quadtree_insert_many.restype = None

        self.lib.quadtree_query_point.argtypes = [
            ctypes.c_void_p,
            ctypes.c_float,
            ctypes.c_float,
            ctypes.POINTER(ctypes.c_size_t),
        ]
        self.lib.quadtree_query_point.restype = ctypes.POINTER(ctypes.c_int)

        self.lib.quadtree_free.argtypes = [ctypes.c_void_p]
        self.lib.quadtree_free.restype = None

        self.tree = self.lib.quadtree_new(x, y, width, height)

    def insert_many(self, rects):
        flat_rects = (ctypes.c_float * len(rects))(*rects)
        self.lib.quadtree_insert_many(self.tree, flat_rects, len(rects))

    def query_point(self, x, y):
        length = ctypes.c_size_t()
        ids_ptr = self.lib.quadtree_query_point(self.tree, x, y, ctypes.byref(length))
        if not ids_ptr:
            return []
        ids = [ids_ptr[i] for i in range(length.value)]
        return ids

    def __del__(self):
        if self.tree:
            self.lib.quadtree_free(self.tree)
