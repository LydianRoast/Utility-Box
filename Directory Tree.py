import os

def generate_directory_tree(path, prefix=""):
    """
    Recursively generate a directory tree structure as a string.

    :param path: Root path of the directory to generate the tree for.
    :param prefix: Prefix used for formatting the tree structure.
    :return: A string representing the directory tree.
    """
    tree = ""
    contents = os.listdir(path)
    contents = sorted(contents, key=lambda x: os.path.isfile(os.path.join(path, x)))

    for index, name in enumerate(contents):
        full_path = os.path.join(path, name)
        connector = "├── " if index < len(contents) - 1 else "└── "
        tree += f"{prefix}{connector}{name}\n"

        if os.path.isdir(full_path):
            tree += generate_directory_tree(full_path, prefix + ("│   " if index < len(contents) - 1 else "    "))
    
    return tree

# Define the path to the root of the project folder
project_path = r'C:\Users\Kevin\Desktop\Mackbot'  # Replace with the actual path to your project folder

# Generate the directory tree
directory_tree = generate_directory_tree(project_path)

# Create a text file and write the directory tree to it using UTF-8 encoding
output_file = "generated_project_directory_structure.txt"
with open(output_file, "w", encoding="utf-8") as f:
    f.write(directory_tree)

print(f"Directory tree saved to {output_file}")
