import threading
import contextlib


context = threading.local()


@contextlib.contextmanager
def new_context(*, ns, ts, fs, exit_on_error):
    context.ns = ns
    context.ts = ts
    context.fs = fs
    context.exit_on_error = exit_on_error
    yield
