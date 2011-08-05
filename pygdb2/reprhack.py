import ctypes

class PyObject(ctypes.Structure):
    _fields_ = [
        ("ob_refcnt", ctypes.c_int),
        ("ob_type", ctypes.py_object)
        ]

class PyObjectVar(PyObject):
    _fields_ = [
        ("ob_size", ctypes.c_ssize_t),
        ]

reprfunc = ctypes.CFUNCTYPE(ctypes.py_object, ctypes.py_object)

class PyTypeObject(PyObjectVar):
    _fields_ = [
        ("tp_name", ctypes.c_char_p),
        ("tp_basicsize", ctypes.c_ssize_t),
        ("tp_itemsize", ctypes.c_ssize_t),
        ("tp_dealloc", ctypes.c_void_p),
        ("tp_print", ctypes.c_void_p),
        ("tp_getattr", ctypes.c_void_p),
        ("tp_setattr", ctypes.c_void_p),
        ("tp_compare", ctypes.c_void_p),
        ("tp_repr", reprfunc),
        ]
    
PyObjectPtr = ctypes.POINTER(PyObject)
PyTypeObjectPtr = ctypes.POINTER(PyTypeObject)

keepalive = []
def patch_repr(mytype):
    def decorator(func):
        p = ctypes.cast(id(mytype), PyTypeObjectPtr)
        cfunc = reprfunc(func)
        keepalive.append(cfunc)
        p.contents.tp_repr = cfunc
        return func
    return decorator

def sanity_check():
    plist = ctypes.cast(id(list), PyTypeObjectPtr)
    refcnt = plist.contents.ob_refcnt
    x = list # incref
    assert plist.contents.ob_refcnt == refcnt+1
    assert plist.contents.ob_type is type
    assert plist.contents.tp_name == 'list'


sanity_check()
