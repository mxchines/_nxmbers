import os
from pathlib import Path

def get_project_path(file_path):
    """
    Get the project path based on the current file's location.
    
    :param file_path: The __file__ variable of the current script
    :return: Path object pointing to the project root (nxmbers folder)
    """
    current_file = Path(file_path).resolve()
    project_root = current_file.parent
    while project_root.name != 'nxmbers':
        project_root = project_root.parent
        if project_root == project_root.parent:  # reached the root of the filesystem
            raise ValueError("Could not find 'nxmbers' directory in the path")
    return project_root

def get_data_path(file_path, filename):
    """
    Get the full path for a data file within the project.
    
    :param file_path: The __file__ variable of the current script
    :param filename: Name of the file to be saved/loaded
    :return: Full path to the data file
    """
    project_root = get_project_path(file_path)
    data_dir = project_root / 'nxmbers' / 'data'
    data_dir.mkdir(parents=True, exist_ok=True)
    return data_dir / filename

# Usage example (to be added at the top of each script that needs it):
# from path_utility import get_data_path