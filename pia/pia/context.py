import threading
import contextlib


context = threading.local()


@contextlib.contextmanager
def new_context(*, env, exit_on_error, module_paths, loaded_lines):
    context.env = env
    context.exit_on_error = exit_on_error
    context.module_paths = module_paths
    context.parent = None
    context.loaded_lines = loaded_lines or []
    yield


def modified_context_args():
    return {
        key: getattr(context, key)
        for key in (
            "env", "exit_on_error", "module_paths", "loaded_lines")
    }
