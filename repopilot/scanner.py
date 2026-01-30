class DirectoryScanner:
    def __init__(self, target_directory):
        self.target_directory = target_directory
        self.structure = {}

    def scan(self):
        self._scan_directory(self.target_directory, self.structure)

    def _scan_directory(self, current_directory, structure):
        import os

        for item in os.listdir(current_directory):
            item_path = os.path.join(current_directory, item)
            if os.path.isdir(item_path):
                structure[item] = {}
                self._scan_directory(item_path, structure[item])
            else:
                structure[item] = None

    def get_structure(self):
        return self.structure

    def print_structure(self, structure=None, indent=0):
        if structure is None:
            structure = self.structure
        for key in structure:
            print('    ' * indent + key)
            if isinstance(structure[key], dict):
                self.print_structure(structure[key], indent + 1)