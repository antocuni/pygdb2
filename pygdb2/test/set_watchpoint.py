import ctypes
import pygdb2

def main():
    print 'program starting'
    buf = ctypes.c_int()
    buf.value = 42
    adr = ctypes.cast(ctypes.pointer(buf), ctypes.c_void_p)
    pygdb2.execute("watch *(int*)%d" % adr.value) # enter gdb when we write to this memory

    i = 0
    while i < 5:
        print i
        i += 1
        if i == 2:
            buf.value = 43 # we should enter gdb here
    print 'program stopping'

if __name__ == '__main__':
    main()
