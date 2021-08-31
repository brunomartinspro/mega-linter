#!/usr/bin/env python3
"""
Output results in console
"""
import copy
import json
import logging
import os
from shutil import copyfile

import jsonpickle
from megalinter import Reporter, config


class ConfigReporter(Reporter):
    name = "CONFIG"
    scope = "mega-linter"
  
    def __init__(self, params=None):
        # Deactivate JSON output by default
        self.is_active = True
        self.processing_order = 9
        super().__init__(params)

    def manage_activation(self):
        if config.get("CONFIG_REPORTER", "true") == "false":
            self.is_active = False

    def produce_report(self):
        config_report_folder_name = config.get("CONFIG_REPORTER_SUB_FOLDER", "IDE-config")
        config_report_folder = f"{self.report_folder}{os.path.sep}{config_report_folder_name}"
        os.makedirs(config_report_folder, exist_ok=True)

        # Collect info from linters execution
        config_log = []
        vscode_recommended_extensions = []
        idea_recommended_extensions = []
        for linter in self.master.linters:
            if linter.is_active is True:
                ide = getattr(linter,"ide",{})
                # add in log
                config_log+= [
                    "",
                    f"{linter.linter_name} ({linter.descriptor_id})"
                ]
                for ide_name,ide_extensions in ide.items():
                    config_log+= [f"  - {ide_name}:"]
                    for ide_extension in ide_extensions:
                        config_log += [f"    - {ide_extension['name']}: {ide_extension['url']}"]
                # Get applicable VsCode extensions
                vscode_extensions = getattr(ide,"vscode",[])
                for vscode_extension in vscode_extensions:
                    if "?itemName=" in vscode_extension['url']:
                        vscode_recommended_extensions += vscode_extension['url'].split("?itemName=",1)[1]
                # Get applicable IDEA extensions
                idea_extensions = getattr(ide,"idea",[])
                for idea_extension in idea_extensions:
                    if "https://plugins.jetbrains.com/plugin/" in idea_extension['url']:
                        idea_recommended_extensions += idea_extension['url'].split("https://plugins.jetbrains.com/plugin/",1)[1]                
        
        # Copy config file if default
        if linter.final_config_file is not None:
            target_config_file = f"{config_report_folder}{os.path.sep}{os.path.basename(linter.final_config_file)}"
            copyfile(linter.final_config_file, target_config_file)

        # Write config log file
        config_report_log = f"{self.report_folder}{os.path.sep}IDE-config.txt"
        config_log_str = "\n".join(config_log)
        config_log_text_full = f"""Mega-Linter can help you to define the same linter configuration locally

INSTRUCTIONS

- Copy the content of IDE-config folder at the root of your repository
- Install the related extensions on your preferred IDE
  - if you are using Visual Studio Code, just reopen your project after the copy, and you will be prompted to install recommended extensions)

IDE EXTENSIONS APPLICABLE TO YOUR PROJECT
{config_log_str}
"""
        with open(config_report_log, "w", encoding="utf-8") as text_file:
            text_file.write(config_log_text_full)

        # Write vscode extensions file
        if len(vscode_recommended_extensions) > 0:
            # Read existing .vscode/extensions.json file
            vscode_extensions_file = f"{self.master.workspace}{os.path.sep}.vscode{os.path.sep}extensions.json"
            if os.path.isfile(vscode_extensions_file):
                with open(vscode_extensions_file, "r", encoding="utf-8") as json_file:
                    vscode_extensions_config = json.load(json_file)
            else:
                vscode_extensions_config = {}
            # Add recommendations
            vscode_extensions_config_recommendations = vscode_extensions_config.get("recommendations",[])
            vscode_extensions_config["recommendations"] = list(set(vscode_extensions_config_recommendations))
            # Write .vscode/extensions.json file
            vscode_extensions_config_json = json.dumps(vscode_extensions_config, sort_keys=True, indent=4)
            with open(vscode_extensions_file, "w", encoding="utf-8") as json_file:
                json_file.write(vscode_extensions_config_json)
        
        # Write idea plugin recommendations files (TODO)
