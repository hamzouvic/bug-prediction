import os
import re
import subprocess

# Define paths
UND_DB_PATH = r"C:\Users\sif\Desktop\mgl869\metrics\db"  # Change this to your preferred path
REPO_PATH = r"C:\Users\sif\Desktop\mgl869\metrics\hive"  # Path to your Git repository
METRICS_REPORT_PATH = r'C:\Users\sif\Desktop\mgl869\metrics\metrics_reports'
GENERATE_METRICS_FILE = r"C:\Users\sif\Desktop\mgl869\metrics\generate_metrics.txt"  # File to store Understand commands

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

# Generate Understand metrics command file for each tag
def generate_metrics_command_file():
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

        print(f"checkout to tag: {tag}")
        subprocess.run(["git", "-C", REPO_PATH, "checkout", tag], check=True)

        print(f"Adding commands for tag: {tag}")

        # Define the Understand database file path for this tag
        und_db = os.path.join(UND_DB_PATH, f"my_project_{version}.und")
        metrics_file = os.path.join(METRICS_REPORT_PATH, f"metrics_{version}.csv")

        # Write commands to create, add files, set settings, analyze, and generate metrics
        with open(GENERATE_METRICS_FILE, "w") as f:
            f.write(f"create -languages C++ Java {und_db}\n")
            f.write(f"add {REPO_PATH}\n")
            f.write(f"settings -metrics all \n")
            f.write(f"settings -metricsOutputFile {metrics_file}\n")
            f.write(f"analyze\n")
            f.write(f"metrics\n")
        print(f'generate metrics for {tag}')
        try:
            print("Running Understand commands from generate_metrics.txt...")
            subprocess.run(["und", "generate_metrics.txt"], check=True)
            print("Understand commands executed successfully.")
        except subprocess.CalledProcessError as e:
            print(f"Error occurred while running Understand commands: {e}")
        print('-------------------------------------------------')

# Run the script
if __name__ == "__main__":
    generate_metrics_command_file()
