# GitHub Folder Downloader CLI

A Python-based CLI tool to download a specific folder from any GitHub repository directly as a .zip file, without the need to clone the entire repository.

## Why This Script?

Imagine you need a single folder from a large repository on GitHub, which has thousands of folders and files. The usual approach would involve cloning the entire repository, then manually removing everything except the target folder—an inefficient and tedious process.

While there are online tools (like [DownGit](https://downgit.github.io) or [download-directory](https://download-directory.github.io)) that solve this problem, these solutions have limitations. For instance:

- They cannot be curled or wgeted directly, which is inconvenient when working in a command-line environment, especially within VMs or Docker containers.
- If you're working in an isolated environment, downloading via browser and then transferring files manually can be time-consuming and error-prone.

This CLI tool was created to solve these issues. It lets you download only the folder you need from GitHub as a .zip file, directly from the command line.

## Features

- Download a single folder from any public GitHub repository.
- No need to clone the entire repository.
- Fully CLI-based, so it can be used directly on remote servers or in containers.
- Outputs the specified folder in a .zip file named after the folder (or as specified with -o).

## Usage

```bash
python3 gethub.py <GitHub URL to the folder> [-o OUTPUT]
```

## Arguments

- `<GitHub URL to the folder>`: The URL of the folder you want to download, in the format:

```bash
https://github.com/<username>/<repo>/tree/<branch or commit>/<path/to/folder>
```

- `-o OUTPUT`: (**Optional**) The name of the output .zip file. If omitted, the .zip file will be named after the folder.

## How It Works

- The script parses the GitHub URL to extract the repository, branch (or commit), and folder path.
- It downloads the repository archive for the specified branch or commit.
- The script extracts only the specified folder and repackages it into a .zip file, which can be saved under a custom name.

## Example Use Cases

- Working with large repositories: Download only the files you need without wasting bandwidth or storage.
- Remote environments: Ideal for downloading resources directly into Docker containers, VMs, or cloud instances without GUI access.
- Automating setup processes: Use the CLI tool in scripts for automated provisioning, setup, or CI/CD.

## Troubleshooting

- Ensure the GitHub URL format is correct.
- The target repository and folder must be public (private repos are not supported).
- Double-check that the branch or commit identifier in the URL is valid.

This CLI tool is designed to save time and streamline the process of downloading specific folders from GitHub. Enjoy, and feel free to contribute! 🚀😊