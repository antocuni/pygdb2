import py
import os
import sys
import re
import pexpect

def expect_lines(child, *lines):
    for line in lines:
        child.expect(line)

def test_set_watchpoint(monkeypatch):
    root = py.path.local(__file__).join('..', '..', '..')
    PYTHONPATH = os.getenv('PYTHONPATH') or ''
    if PYTHONPATH:
        PYTHONPATH += ':'
    PYTHONPATH += str(root)
    monkeypatch.setenv('PYTHONPATH', PYTHONPATH)
    #
    watch_expr = re.escape('*(int*)') + '[0-9]*'
    #
    cmd = 'gdb --eval "python import pygdb2" --args %s set_watchpoint.py' % sys.executable
    child = pexpect.spawn(cmd, timeout=2)
    child.logfile = sys.stdout
    child.expect_exact ('(gdb) ')
    child.sendline('pyrun')
    expect_lines(child,
                 'program starting',
                 'pygdb2: watch %s' % watch_expr,
                 'Hardware watchpoint 1: %s' % watch_expr,
                 '0',
                 '1',
                 'Hardware watchpoint 1: %s' % watch_expr,
                 'Old value = 42',
                 'New value = 43',
                 )
    child.expect_exact ('(gdb) ')
    child.sendline('c')
    expect_lines(child,
                 '2',
                 '3',
                 '4',
                 'program stopping',
                 )
    child.expect_exact('Program exited normally.')
    child.expect_exact ('(gdb) ')
    child.sendline('quit')
    child.expect(pexpect.EOF)
