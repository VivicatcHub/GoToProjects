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

    def write(self, content: str):
        """Writes content to the script file."""
        self.script_file.write(content)

    def echo(self, content: str):
        """Writes an echo command to the script file."""
        self.script_file.write(f"echo '{content}'\n")

    def cd(self, path: str):
        """Writes a cd command to the script file."""
        self.script_file.write(f"cd '{path}'\n")

    def pull(self):
        """Writes a git pull command to the script file."""
        self.script_file.write("git pull\n")

    def vscode(self, path: str):
        """Writes a command to open the project in VSCode."""
        self.script_file.write(f"code '{path}'\n")

    def generate_script(self):
        """Generates the script for the specified project."""
        self.script_file.write("#!/bin/zsh\n")

        if self.project_name in self.projects:
            self.generate_script_for_project(self.projects[self.project_name])
        else:
            self.echo(f"❓ Project '{self.project_name}' not found.")
            available_projects = [project for project in self.projects.keys() if project[0] == self.project_name[0]]
            self.echo(f"📋 Available projects: {', '.join(available_projects) if available_projects else 'None'}")

    def generate_script_for_project(self, project):
        """Generates the script for the specified project."""
        self.echo(f"🚀 Navigating to project: {self.project_name}")
        self.echo(f"📁 Path: {project['path']}")
        self.cd(project["path"])

        if project.get("pull"):
            self.echo("🔄 Pulling latest changes...")
            self.pull()

        for command in project["commands"]:
            if command[:4] != "echo":
                self.echo(f"💻 Executing command: {command}")
            self.script_file.write(f"{command}\n")

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
