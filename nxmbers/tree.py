import os

def print_directory_tree(path, prefix=""):
    """Recursively prints a directory tree, ignoring hidden files."""

    entries = [entry for entry in os.listdir(path) if not entry.startswith('.')]
    entries.sort() 
    num_entries = len(entries)

    for index, entry in enumerate(entries):
        entry_path = os.path.join(path, entry)
        if os.path.isdir(entry_path):
            # Directory
            connector = "└── " if index == num_entries - 1 else "├── "
            print(prefix + connector + entry)
            print_directory_tree(entry_path, prefix + ("    " if index == num_entries - 1 else "│   "))
        else:
            # File
            connector = "└── " if index == num_entries - 1 else "├── "
            print(prefix + connector + entry)

# Start from the current directory
start_path = "."
print_directory_tree(start_path)