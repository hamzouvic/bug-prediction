import subprocess
import os
import re

# Define paths
UND_DB_PATH = r"C:\Users\sif\Desktop\mgl869\metrics\db"  # Change this to your preferred path
REPO_PATH = r"C:\Users\sif\Desktop\mgl869\metrics\hive"         # Path to your Git repository
METRICS_REPORT_PATH = os.path.join(REPO_PATH, "metrics_reports")

# Define the starting version
START_VERSION = "2.0.0"

# Regex pattern to match tags in the format rel/release-X.Y.Z and skip pre-release versions
tag_pattern = re.compile(r"^rel/release-(\d+\.\d+\.\d+)$")

# Create directory for metrics reports if it doesn't exist
os.makedirs(METRICS_REPORT_PATH, exist_ok=True)

# Get the list of tags from the repository
def get_git_tags():
    tags = subprocess.check_output(["git", "-C", REPO_PATH, "tag"], text=True).splitlines()
    return tags

# Check if the tag version is greater or equal to START_VERSION
def is_version_greater_or_equal(version, start_version=START_VERSION):
    return tuple(map(int, version.split('.'))) >= tuple(map(int, start_version.split('.')))

# Generate Understand metrics report for each tag
def generate_metrics_for_tags():
    tags = get_git_tags()
    start_processing = False

    for tag in tags:
        match = tag_pattern.match(tag)
        if not match:
            continue  # Skip tags that don't match the required format

        version = match.group(1)
        
        if is_version_greater_or_equal(version):
            start_processing = True

        if not start_processing:
            continue

        print(f"Processing tag: {tag}")

        # Checkout the tag
        subprocess.run(["git", "-C", REPO_PATH, "checkout", tag], check=True)

        # Define the Understand database file path for this tag
        und_db = os.path.join(UND_DB_PATH, f"my_project_{version}.udb")

        # Create a new Understand database
        subprocess.run(["und", "create", "-db", und_db], check=True)

        # Add files to the Understand database
        subprocess.run(["und", "-db", und_db, "add", REPO_PATH], check=True)

        # Analyze the Understand database
        subprocess.run(["und", "analyze", "-db", und_db], check=True)

        # Generate metrics report and save it to a file
        metrics_file = os.path.join(METRICS_REPORT_PATH, f"metrics_{version}.txt")
        with open(metrics_file, "w") as f:
            subprocess.run(["und", "report", "-db", und_db, "-metrics"], stdout=f, check=True)

        print(f"Metrics report generated for tag: {tag}")

    # Checkout back to the main branch
    subprocess.run(["git", "-C", REPO_PATH, "checkout", "master"], check=True)

# Run the script
if __name__ == "__main__":
    generate_metrics_for_tags()
