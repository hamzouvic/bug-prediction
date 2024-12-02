import subprocess
import re

REPO_PATH = r"C:\Users\sif\Desktop\mgl869\metrics\hive"         # Path to your Git repository
START_VERSION = '2.0.0'
def get_git_tags():
    tags = subprocess.check_output(["git", "-C", REPO_PATH, "tag"], text=True).splitlines()
    return tags

def is_version_greater_or_equal(version, start_version=START_VERSION):
    version_major_minor = tuple(map(int, version.split('.')[:2]))
    start_major_minor = tuple(map(int, start_version.split('.')[:2]))
    return version_major_minor >= start_major_minor


tag_pattern = re.compile(r"^rel/release-(\d+\.\d+\.\d+)$")

tags = get_git_tags()
selected_tags = []
seen_major_minor = set()

for tag in tags:
    match = tag_pattern.match(tag)
    if not match:
        continue  # Skip tags that don't match the required format

    version = match.group(1)  # Extract version string from tag
    major_minor = ".".join(version.split('.')[:2])  # Extract major.minor

    if is_version_greater_or_equal(version) and major_minor not in seen_major_minor:
        selected_tags.append(tag)
        seen_major_minor.add(major_minor)
print(selected_tags)
  

