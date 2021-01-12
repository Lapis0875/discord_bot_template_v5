from typing import Dict


__all__ = (
    'parsePyFileName',
    'parseCogName'
)


def parsePyFileName(file: str) -> str:
    """Parse python code file name from __file__
    Args:
        file (str): value which can be got using '__file__'
    Returns:
        filename (str): Parsed string value of file name.
    """
    return file.split('/')[-1].strip('.py')


def parseCogName(ext_map: Dict[str, Dict[str, str]], module_path: str) -> str:

    return [key for key, value in ext_map.get(module_path.split('.')[1]).items() if value == module_path][0]
