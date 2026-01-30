def analyze_directory_structure(directory):
    import os
    from collections import Counter

    file_types = Counter()

    for root, dirs, files in os.walk(directory):
        for file in files:
            ext = os.path.splitext(file)[1]
            if ext in ['.py', '.js', '.md', '.json', '.html']:
                file_types[ext] += 1

    return file_types


def generate_summary(file_types):
    summary = {
        "total_files": sum(file_types.values()),
        "file_type_counts": dict(file_types),
        "project_description": "This project is an AI-powered developer workflow assistant.",
        "functionality": "The project includes features for scanning directories, analyzing file types, and generating summaries and reports."
    }
    return summary


def main(directory):
    file_types = analyze_directory_structure(directory)
    summary = generate_summary(file_types)
    return summary


if __name__ == "__main__":
    import sys

    if len(sys.argv) != 2:
        print("Usage: python analyzer.py <directory>")
        sys.exit(1)

    directory = sys.argv[1]
    summary = main(directory)
    print(summary)