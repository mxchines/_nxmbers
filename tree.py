import os

def print_directory_tree(path, prefix=""):
    """Recursively prints a directory tree, excluding hidden files."""

    # Get only non-hidden entries
    entries = [entry for entry in os.listdir(path) if not entry.startswith('.')]

    # Sort the entries
    entries.sort()

    # Get the number of entries
    num_entries = len(entries)

    for index, entry in enumerate(entries):
        # Construct the full path of the entry
        entry_path = os.path.join(path, entry)

        # Check if the entry is a directory
        if os.path.isdir(entry_path):
            # Directory
            connector = "└── " if index == num_entries - 1 else "├── "
            print(prefix + connector + entry)
            # Recursively print the directory tree
            print_directory_tree(entry_path, prefix + ("    " if index == num_entries - 1 else "│   "))
        else:
            # File
            connector = "└── " if index == num_entries - 1 else "├── "
            print(prefix + connector + entry)

# Start from the current directory
start_path = "."
print_directory_tree(start_path)