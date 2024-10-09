from pathlib import Path
from typing import Dict, Union
from dataclasses import dataclass

@dataclass
class ProjectPaths:
    """
    Dataclass containing all project paths.
    This provides easy access to all project paths as attributes.
    """
    root: Path
    data: Path
    csv: Path
    plots: Path
    cleaned: Path
    r_scripts: Path
    templates: Path

class PathManager:
    """
    Singleton class to manage all paths in the project.
    Ensures consistent path handling across all modules.
    """
    _instance = None
    _paths: ProjectPaths = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(PathManager, cls).__new__(cls)
            cls._instance._initialize_paths()
        return cls._instance

    def _initialize_paths(self) -> None:
        """Initialize all project paths."""
        # Find project root
        current_file = Path(__file__).resolve()
        root = current_file.parent
        while root.name != 'nxmbers':
            root = root.parent
            if root == root.parent:  # reached the filesystem root
                raise ValueError("Could not find 'nxmbers' directory in the path")

        # Define all project paths
        self._paths = ProjectPaths(
            root=root,
            data=root / "nxmbers" / "data",
            csv=root / "nxmbers" / "data" / "csv",
            plots=root / "nxmbers" / "data" / "plots",
            cleaned=root / "nxmbers" / "data" / "cleaned",
            r_scripts=root / "nxmbers" / "R",
            templates=root / "nxmbers" / "templates"
        )
        
        # Create all directories
        self._create_directories()

    def _create_directories(self) -> None:
        """Create all necessary directories if they don't exist."""
        for path in [self._paths.data, self._paths.csv, self._paths.plots, 
                    self._paths.cleaned, self._paths.r_scripts, self._paths.templates]:
            path.mkdir(parents=True, exist_ok=True)

    @property
    def paths(self) -> ProjectPaths:
        """Get all project paths."""
        return self._paths

    def get_path(self, name: str) -> Path:
        """
        Get a specific path by name.
        
        Args:
            name: The name of the path to get (e.g., 'csv', 'plots')
        
        Returns:
            Path object for the requested path
        """
        return getattr(self._paths, name)

    def get_file_path(self, directory: str, filename: str) -> Path:
        """
        Get full path for a file within a specified directory.
        
        Args:
            directory: The directory name (e.g., 'csv', 'plots')
            filename: The name of the file
        
        Returns:
            Full path to the specified file
        """
        return self.get_path(directory) / filename

# Create global instance
path_manager = PathManager()

# New interface functions
def get_all_paths() -> ProjectPaths:
    """Get all project paths as a ProjectPaths object."""
    return path_manager.paths

def get_path(name: str) -> Path:
    """
    Get a specific path by name.
    
    Example:
    >>> get_path('csv')
    PosixPath('/path/to/nxmbers/data/csv')
    """
    return path_manager.get_path(name)

def get_file_path(directory: str, filename: str) -> Path:
    """
    Get full path for a file within a specified directory.
    
    Example:
    >>> get_file_path('csv', 'my_data.csv')
    PosixPath('/path/to/nxmbers/data/csv/my_data.csv')
    """
    return path_manager.get_file_path(directory, filename)

# Legacy interface functions
def get_project_path(file_path: str) -> Path:
    """
    Maintain compatibility with existing code.
    The file_path parameter is ignored but kept for compatibility.
    
    Example:
    >>> get_project_path(__file__)
    PosixPath('/path/to/nxmbers')
    """
    return path_manager.paths.root

def get_data_path(file_path: str, filename: str) -> Path:
    """
    Maintain compatibility with existing code.
    The file_path parameter is ignored but kept for compatibility.
    
    Example:
    >>> get_data_path(__file__, 'my_data.csv')
    PosixPath('/path/to/nxmbers/data/my_data.csv')
    """
    return path_manager.paths.data / filename

# Example usage in doctest format
def _test():
    """
    >>> paths = get_all_paths()
    >>> str(paths.csv).endswith('nxmbers/data/csv')
    True
    >>> str(get_path('plots')).endswith('nxmbers/data/plots')
    True
    >>> str(get_file_path('csv', 'data.csv')).endswith('nxmbers/data/csv/data.csv')
    True
    >>> str(get_data_path(__file__, 'old_style.csv')).endswith('nxmbers/data/old_style.csv')
    True
    """
    pass

if __name__ == '__main__':
    import doctest
    doctest.testmod()