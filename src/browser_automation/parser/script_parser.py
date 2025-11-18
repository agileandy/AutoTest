"""YAML test script parser for browser automation."""
import yaml
from pathlib import Path
from typing import Dict, List, Any, Optional
from dataclasses import dataclass


@dataclass
class TestStep:
    """Represents a single test step."""
    action: str
    params: Dict[str, Any]

    def __init__(self, action: str, **kwargs):
        self.action = action
        self.params = kwargs


@dataclass
class TestScript:
    """Represents a complete test script."""
    name: str
    description: str
    base_url: str
    headless: bool
    steps: List[TestStep]
    timeout: int = 30000
    screenshot_on_failure: bool = True

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'TestScript':
        """Create TestScript from dictionary."""
        steps = [
            TestStep(action=step.pop('action'), **step)
            for step in data.get('steps', [])
        ]

        return cls(
            name=data.get('name', 'Unnamed Test'),
            description=data.get('description', ''),
            base_url=data.get('base_url', 'http://localhost:5000'),
            headless=data.get('headless', True),
            timeout=data.get('timeout', 30000),
            screenshot_on_failure=data.get('screenshot_on_failure', True),
            steps=steps
        )


class ScriptParser:
    """Parser for YAML test scripts."""

    @staticmethod
    def parse_file(file_path: str) -> TestScript:
        """
        Parse a YAML test script file.

        Args:
            file_path: Path to the YAML file

        Returns:
            TestScript object

        Raises:
            FileNotFoundError: If file doesn't exist
            yaml.YAMLError: If YAML is invalid
            ValueError: If script structure is invalid
        """
        path = Path(file_path)
        if not path.exists():
            raise FileNotFoundError(f"Test script not found: {file_path}")

        with path.open('r') as f:
            data = yaml.safe_load(f)

        if not isinstance(data, dict):
            raise ValueError("Test script must be a YAML dictionary")

        return TestScript.from_dict(data)

    @staticmethod
    def validate_script(script: TestScript) -> List[str]:
        """
        Validate a test script and return any errors.

        Args:
            script: TestScript to validate

        Returns:
            List of validation error messages (empty if valid)
        """
        errors = []

        if not script.name:
            errors.append("Script must have a name")

        if not script.steps:
            errors.append("Script must have at least one step")

        # Validate each step has required parameters
        valid_actions = {
            'navigate': ['url'],
            'click': ['selector'],
            'type': ['selector', 'text'],
            'wait_for_selector': ['selector'],
            'assert_text': ['selector', 'expected'],
            'assert_visible': ['selector'],
            'upload_file': ['selector', 'file_path'],
            'screenshot': ['filename'],
            'wait': ['ms'],
            'select_option': ['selector', 'value'],
            'check': ['selector'],
            'uncheck': ['selector'],
            'hover': ['selector'],
            'press': ['selector', 'key'],
            'evaluate_js': ['script'],
            'count_elements': ['selector'],
            'assert_count': ['selector', 'expected'],
            'assert_min_count': ['selector', 'minimum'],
            'get_text': ['selector'],
        }

        for i, step in enumerate(script.steps, 1):
            if step.action not in valid_actions:
                errors.append(f"Step {i}: Unknown action '{step.action}'")
                continue

            required_params = valid_actions[step.action]
            missing = [p for p in required_params if p not in step.params]
            if missing:
                errors.append(
                    f"Step {i}: Action '{step.action}' missing required parameters: {missing}"
                )

        return errors
