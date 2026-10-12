import pytest


def pytest_configure(config):
    """Work around gltest-direct's temporary stdin file cleanup on Windows."""
    import os

    if os.name != "nt":
        return

    try:
        from gltest.direct import loader
        from gltest.direct.vm import VMContext
    except ImportError:
        return

    original_inject = loader._inject_message_to_fd0
    original_cleanup = VMContext._cleanup_after_deactivate
    original_unlink = os.unlink
    pending_paths = set()

    def defer_locked_temp_file(path, *args, **kwargs):
        try:
            return original_unlink(path, *args, **kwargs)
        except PermissionError:
            pending_paths.add(os.fspath(path))

    def windows_inject(vm):
        os.unlink = defer_locked_temp_file
        try:
            return original_inject(vm)
        finally:
            os.unlink = original_unlink

    def cleanup_after_deactivate(vm):
        try:
            return original_cleanup(vm)
        finally:
            for path in tuple(pending_paths):
                try:
                    original_unlink(path)
                except FileNotFoundError:
                    pass
                finally:
                    pending_paths.discard(path)

    loader._inject_message_to_fd0 = windows_inject
    VMContext._cleanup_after_deactivate = cleanup_after_deactivate


@pytest.fixture(autouse=True)
def _reset_contract_registry():
    yield
    try:
        import genlayer.gl.genvm_contracts as contracts
    except ImportError:
        return
    contracts.__known_contract__ = None
