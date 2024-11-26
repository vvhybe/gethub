import requests
import zipfile
import io
import argparse
import os
from pathlib import Path
import re

GITHUB_API_URL = "https://api.github.com/repos"

def download_and_zip_folder(repo, folder_path, ref, output_name):
    # Step 1: Download the repo archive zip file for the specific branch or commit
    download_url = f"https://github.com/{repo}/archive/{ref}.zip"
    response = requests.get(download_url)
    if response.status_code != 200:
        raise Exception(f"Failed to download repository archive: {response.status_code}")

    # Step 2: Extract only the target folder from the archive
    with zipfile.ZipFile(io.BytesIO(response.content)) as zip_file:
        # Get the top-level directory (name format: {repo}-{ref})
        top_dir = zip_file.namelist()[0].split('/')[0]
        extracted_folder_name = Path(folder_path).name

        # Temporary folder to hold extracted contents
        temp_dir = Path(output_name).stem
        os.makedirs(temp_dir, exist_ok=True)

        for member in zip_file.namelist():
            # Extract only files under the specified folder path
            if member.startswith(f"{top_dir}/{folder_path}"):
                relative_path = Path(member).relative_to(top_dir).relative_to(folder_path)
                target_path = Path(temp_dir) / extracted_folder_name / relative_path

                # If the member is a directory, create it
                if member.endswith('/'):
                    target_path.mkdir(parents=True, exist_ok=True)
                else:
                    # Extract file to the target path
                    with zip_file.open(member) as source_file:
                        with open(target_path, "wb") as target_file:
                            target_file.write(source_file.read())

    # Step 3: Zip the extracted folder
    with zipfile.ZipFile(output_name, 'w') as zip_output:
        for root, _, files in os.walk(temp_dir):
            for file in files:
                file_path = Path(root) / file
                zip_output.write(file_path, file_path.relative_to(temp_dir))

    # Cleanup: Remove the temporary extraction folder
    for root, dirs, files in os.walk(temp_dir, topdown=False):
        for file in files:
            os.remove(Path(root) / file)
        for dir in dirs:
            os.rmdir(Path(root) / dir)
    os.rmdir(temp_dir)

    print(f"Successfully created {output_name}")

def main():
    # CLI argument parser
    parser = argparse.ArgumentParser(description="Download a specific folder from a GitHub repo and zip it.")
    parser.add_argument("url", help="GitHub repository URL to the folder")
    parser.add_argument("-o", "--output", help="Output zip file name", default=None)
    args = parser.parse_args()

    # Parse URL
    url_pattern = r"https://github\.com/(?P<username>[^/]+)/(?P<repo>[^/]+)/tree/(?P<ref>[^/]+)/(?P<path>.+)"
    match = re.match(url_pattern, args.url)
    if not match:
        raise ValueError("Invalid GitHub URL format. Please provide a URL in the format: https://github.com/username/repo/tree/branch/path/to/folder")

    # Extract components from the URL
    repo = f"{match.group('username')}/{match.group('repo')}"
    ref = match.group("ref")
    folder_path = match.group("path")

    # Determine output zip file name
    output_name = args.output if args.output else f"{Path(folder_path).name}.zip"

    # Run the download and zip process
    download_and_zip_folder(repo, folder_path, ref, output_name)

if __name__ == "__main__":
    main()