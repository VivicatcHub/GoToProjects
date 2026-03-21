# GoToProjects

A command-line tool to quickly navigate to your development projects and automatically execute predefined commands.

- [French Doc](README.fr.md)

## Table of Contents

- [Features](#features)
- [Project Structure](#project-structure)
- [Installation](#installation)
  - [Option 1: Automatic Installation (Recommended)](#option-1-automatic-installation-recommended)
  - [Option 2: Manual Installation (local usage)](#option-2-manual-installation-local-usage)
- [Configuration](#configuration)
  - [Create your configuration file](#create-your-configuration-file)
  - [Configuration Options](#configuration-options)
- [Usage](#usage)
  - [After installation (recommended)](#after-installation-recommended)
  - [Local usage (without installation)](#local-usage-without-installation)
  - [Examples](#examples)
- [Troubleshooting](#troubleshooting)
  - [Directory change doesn't persist](#directory-change-doesnt-persist)
  - [Project not found](#project-not-found)
  - [Path errors](#path-errors)
  - [Temporary script not generated](#temporary-script-not-generated)
- [Uninstallation](#uninstallation)
- [Technical Information](#technical-information)
  - [Architecture](#architecture)
  - [Temporary Files](#temporary-files)
- [Version History](#version-history)
- [Contributing](#contributing)
- [License](#license)

## Features

- 🚀 Quick navigation to your projects
- 📂 Persistent directory changes in the shell
- 🔄 Automatic Git pull of latest changes
- 💻 Automatic execution of custom commands
- 🖥️ Automatic opening in VS Code
- ⚙️ Flexible JSON configuration

## Project Structure

```
GoToProjects/
├── go_to_project.py     # Main Python script
├── gtp                  # Shell wrapper script
├── install.sh           # Installation script
├── config.json          # Project configuration
├── config_example.json  # Configuration example
├── requirements.txt     # Python dependencies
└── README.md            # This file
```

## Installation

### Option 1: Automatic Installation (Recommended)

1. Clone or download this repository

```bash
git clone https://github.com/VivicatcHub/GoToProjects.git
cd GoToProjects
```

2. Run the installation script (requires sudo):

```bash
sudo ./install.sh
```

3. The script will:
   - Verify that all necessary files exist
   - Create a `gtp` script with integrated absolute paths
   - Install it to `/usr/bin/gtp`
   - Make the binary accessible from anywhere

### Option 2: Manual Installation (local usage)

If you prefer to use the tool without system installation:

```bash
# From the GoToProjects directory
source ./gtp <project_name>
```

This method doesn't require root privileges but only works from the project directory.

## Configuration

### Create your configuration file

1. Copy the example file:

```bash
cp config_example.json config.json
```

2. Edit `config.json` according to your projects:

```json
{
  "my-project": {
    "path": "/home/user/Projects/my-project/",
    "vscode": true,
    "pull": true,
    "commands": ["npm install", "npm run dev"]
  },
  "another-project": {
    "path": "/home/user/Work/another-project/",
    "vscode": false,
    "pull": false,
    "commands": ["docker-compose up -d", "echo 'Project started!'"]
  }
}
```

### Configuration Options

For each project, you can define:

- **`path`** (required): Absolute path to the project directory
- **`vscode`** (optional): `true` to automatically open VS Code
- **`pull`** (optional): `true` to automatically execute `git pull`
- **`commands`** (optional): List of commands to execute in order

## Usage

### After installation (recommended)

Simply use the `gtp` command from anywhere:

```bash
gtp <project-name>
```

### Local usage (without installation)

From the GoToProjects directory:

```bash
source ./gtp <project-name>
```

### Examples

```bash
# Go to project "wow"
gtp wow

# The script will:
# 1. Navigate to /incredible/wow
# 2. Execute git pull (if pull: true)
# 3. Execute all defined commands in order
# 4. Open VS Code (if vscode: true)
```

## Troubleshooting

### Directory change doesn't persist

**Problem**: After running `gtp`, you're still in the original directory.

**Solutions**:

- ✅ Use `gtp <project>` after system installation
- ✅ Use `source ./gtp <project>` for local usage
- ❌ Never use `./gtp <project>` (runs in a subshell)

### Project not found

The script suggests similar projects based on the first letter:

```bash
$ gtp ma
❓ Project 'ma' not found.
📋 Available projects: marin-kitagawa
```

### Path errors

Verify that:

- The path in `config.json` is correct
- You have permissions to access the directory
- The directory exists

### Temporary script not generated

**Problem**: Message "❌ No script generated for project 'X'"

**Possible causes**:

- The project doesn't exist in `config.json`
- Error in the Python script
- Insufficient permissions to write to `/tmp/`

**Solution**: Verify that the project exists and that the `config.json` file is valid.

## Uninstallation

To remove `gtp` from the system:

```bash
sudo rm /usr/bin/gtp
```

## Technical Information

### Architecture

1. **`go_to_project.py`**: Main Python script that:
   - Reads the JSON configuration
   - Generates a temporary shell script with commands
   - Places the script in `/tmp/gtp_<project_name>.sh`

2. **`gtp`**: Shell wrapper script that:
   - Calls the Python script
   - Sources the generated temporary script
   - Cleans up the temporary file

3. **`install.sh`**: Installation script that:
   - Creates a version of `gtp` with absolute paths
   - Installs it to `/usr/bin/`

### Temporary Files

Temporary scripts are created in `/tmp/gtp_<project_name>.sh` and automatically deleted after use.

## Version History

### v1.3 (Current)

- ✅ Case-insensitive project names
- ✅ New `list` command to display all available projects
- ✅ Improved project search with beginning character filtering
- ✅ Better error handling and messages
- ✅ Fix error when project name is not provided

### v1.2

- ✅ Support for the `never_ask` option to execute commands without confirmation
- ✅ Integrated confirmation prompt in the generated bash script (zsh compatible)

### v1.1

- ✅ System installation in `/usr/bin/`
- ✅ Improved error handling
- ✅ Automatic cleanup of temporary files

### v1.0

- ✅ Initial release with zsh function
- ✅ Project support via JSON
- ✅ Custom commands

## License

This project is open source. Feel free to use, modify, and distribute it according to your needs.
