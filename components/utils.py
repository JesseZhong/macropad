from os import stat

def file_exists(filepath: str):
    """
        Check if a file exists.
        CircuitPython does not have path.
    """
    try:
        stat(filepath)
        return True
    except OSError:
        return False