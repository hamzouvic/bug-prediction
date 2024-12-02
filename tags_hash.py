import subprocess
import csv
import re


REPO_PATH = r"C:\Users\sif\Desktop\mgl869\metrics\hive"  # Path to your Git repository

def get_git_tags():
    result = subprocess.run(['git',"-C", REPO_PATH, 'tag'], stdout=subprocess.PIPE, text=True, check=True)
    tags = result.stdout.splitlines()  # Split output into lines (one tag per line)
    return tags

def get_commit_hash(tag):
    result = subprocess.run(['git', "-C", REPO_PATH, 'rev-list', '-n', '1', tag], stdout=subprocess.PIPE, text=True, check=True)
    return result.stdout.strip()  # Remove any extra whitespace

# Step 3: Generate CSV
def generate_csv(output_file):
    tags = get_git_tags()
    seen_versions = set()  # Track seen major.minor versions
    with open(output_file, 'w', newline='') as csvfile:
        csv_writer = csv.writer(csvfile)
        # Write header
        csv_writer.writerow(['Version', 'Commit Hash'])
        for tag in tags:
            version = extract_version(tag)  # Extract version number
            if version and is_first_minor(version, seen_versions):  # Filter first minor occurrence
                commit_hash = get_commit_hash(tag)
                csv_writer.writerow([version, commit_hash])  # Write version and hash
def is_first_minor(version, seen_versions):
    major, minor, _ = map(int, version.split('.'))
    if major < 2:  # Ignore versions before 2.0.0
        return False
    if (major, minor) in seen_versions:  # Skip if minor version is already seen
        return False
    seen_versions.add((major, minor))  # Mark as seen
    return True
def extract_version(tag):
    # Regex to match tags like rel/release-4.0.0 or release-0.13.0
    match = re.match(r'(?:rel/)?release-(\d+\.\d+\.\d+)', tag)
    if match:
        return match.group(1)  # Extract and return the version number (e.g., 4.0.0)
    return None  # Return None if the tag doesn't match the format

# Run the script
if __name__ == "__main__":
    output_file = "git_tags_and_commits.csv"
    generate_csv(output_file)
    print(f"CSV file '{output_file}' has been generated.")
