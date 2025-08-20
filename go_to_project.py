#!/usr/bin/env python3

import os
import sys
import json


class GoToProject:
    """A class to generate a script for navigating to a specified project directory."""

    def __init__(self, project_name: str):
        self.project_name = project_name
        self.script_path = f"/tmp/gtp_{project_name}.sh"
        self.script_file = open(self.script_path, "a")
        if os.path.getsize(self.script_path) > 0:
            self.script_file.close()
            self.script_file = open(self.script_path, "w")
        self.config_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "config.json")
        with open(self.config_path, "r") as file:
            self.projects = json.load(file)

    def write(self, content: str, tab: bool = False):
        """Writes content to the script file."""
        self.script_file.write(f"{'\t' if tab else ''}{content}\n")

    def echo(self, content: str, tab: bool = False):
        """Writes an echo command to the script file."""
        self.write(f"echo '{content}'", tab=tab)

    def cd(self, path: str):
        """Writes a cd command to the script file."""
        self.write(f"cd '{path}'")

    def pull(self):
        """Writes a git pull command to the script file."""
        self.write("git pull")

    def vscode(self, path: str):
        """Writes a command to open the project in VSCode."""
        self.write(f"code '{path}'")

    def generate_script(self):
        """Generates the script for the specified project."""
        self.write("#!/bin/zsh")

        if self.project_name in self.projects:
            self.generate_script_for_project(self.projects[self.project_name])
        else:
            self.echo(f"❓ Project '{self.project_name}' not found.")
            available_projects = [project for project in self.projects.keys() if project[0] == self.project_name[0]]
            self.echo(f"📋 Available projects: {', '.join(available_projects) if available_projects else 'None'}")

    def write_command(self, command: str, tab: bool = False):
        """Writes a command to the script file."""
        if command[:4] != "echo":
            self.echo(f"💻 Executing command: {command}", tab=tab)
        self.write(f"{command}", tab=tab)

    def generate_script_for_project(self, project):
        """Generates the script for the specified project."""
        self.echo(f"🚀 Navigating to project: {self.project_name}")
        self.echo(f"📁 Path: {project['path']}")
        self.cd(project["path"])

        if project.get("pull"):
            self.echo("🔄 Pulling latest changes...")
            self.pull()

        if project.get("never_ask"):
            # Execute commands without asking
            if not project.get("commands"):
                self.echo("❗ No commands to execute.")
            else:
                for command in project.get("commands"):
                    self.write_command(command)
        else:
            # Generate zsh code to ask for confirmation
            self.write('echo -n "Do you want to execute commands? (Y/n): "')
            self.write("read response")
            self.write('if [[ "$response" != "n" && "$response" != "N" ]]; then')
            self.write("echo 'Executing commands...'", tab=True)
            if not project.get("commands"):
                self.echo("❗ No commands to execute.", tab=True)
            else:
                for command in project.get("commands"):
                    self.write_command(command, tab=True)
            self.write("fi")

        if project.get("vscode"):
            self.echo("🖥️ Opening in VSCode...")
            self.vscode(project["path"])


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: go_to_project.py <project_name>")
        sys.exit(1)

    gtp = GoToProject(sys.argv[1])

    try:
        gtp.generate_script()
    except Exception as e:
        print(f"❌ Error generating script: {e}")
        sys.exit(1)
