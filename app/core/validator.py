#Core validation logic for JSON and YAML configuration files.
# Provides methods to validate individual files and all files in a directory.

import json
import yaml
import os
from typing import Tuple, List, Dict, Any
from pathlib import Path

class ConfigValidator:
    def __init__(self):
        # Define required keys for valid configs
        self.required_keys = ["name", "version", "environment"]
        self.valid_environments = ["development", "staging", "production"]

    def validate_content(self, content: str, config_type: str) -> Tuple[bool, List[str]]:
        errors = []

        try:
            if config_type.lower() == "json":
                config_data = json.loads(content)
            elif config_type.lower() in ["yaml", "yml"]:
                config_data = yaml.safe_load(content)
            else:
                return False, [f"Unsupported config type: {config_type}"]

            # Validate structure
            if not isinstance(config_data, dict):
                errors.append("Config must be a dictionary/object")
                return False, errors

            # Check required keys
            for key in self.required_keys:
                if key not in config_data:
                    errors.append(f"Missing required key: '{key}'")

            # Validate environment value
           
            env = config_data["environment"]
            if env not in self.valid_environments:
                errors.append(
                f"Invalid environment '{env}'. Must be one of: {self.valid_environments}")

            # Validate version format (should be string like "1.0.0")
            version = config_data["version"]
            if not isinstance(version, str) or not version:
                errors.append("Version must be a non-empty string")

            return len(errors) == 0, errors

        except json.JSONDecodeError as e:
            return False, [f"Invalid JSON: {str(e)}"]
        except yaml.YAMLError as e:
            return False, [f"Invalid YAML: {str(e)}"]
        except Exception as e:
            return False, [f"Validation error: {str(e)}"]

    def validate_file(self, file_path: str) -> Tuple[bool, List[str]]:
        """
        Validate a configuration file.

        Args:
            file_path: Path to the configuration file

        Returns:
            Tuple of (is_valid, list_of_errors)
        """
        try:
            with open(file_path, 'r') as f:
                content = f.read()

            # Determine type from extension
            ext = Path(file_path).suffix.lower()
            if ext == ".json":
                config_type = "json"
            elif ext in [".yaml", ".yml"]:
                config_type = "yaml"
            else:
                return False, [f"Unsupported file extension: {ext}"]

            return self.validate_content(content, config_type)

        except FileNotFoundError:
            return False, [f"File not found: {file_path}"]
        except Exception as e:
            return False, [f"Error reading file: {str(e)}"]
        

    def validate_all_configs(self, directory: str = "configs") -> List[Dict[str, Any]]:
        results = []
        base = Path(directory)
        if not base.exists():
            return [{"error": f"Directory not found: {base}"}]

        config_files = []
        for ext in (".json", ".yaml", ".yml"):
            config_files.extend(base.glob(f"*{ext}")) 

        if not config_files:
            return [{"warning": f"No config files found in {base}"}]

        for file_path in config_files:
            is_valid, errors = self.validate_file(str(file_path))
            results.append({"file": str(file_path), "valid": is_valid, "errors": errors})

        return results