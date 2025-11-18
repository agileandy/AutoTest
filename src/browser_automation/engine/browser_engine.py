"""Browser automation engine using Playwright."""
import asyncio
from typing import Optional, List, Dict, Any
from pathlib import Path
from datetime import datetime
from playwright.async_api import async_playwright, Browser, BrowserContext, Page

from ..parser.script_parser import TestScript, TestStep
from .actions import BrowserActions


class TestResult:
    """Stores test execution results."""

    def __init__(self, script_name: str):
        self.script_name = script_name
        self.passed = False
        self.error: Optional[str] = None
        self.start_time: Optional[datetime] = None
        self.end_time: Optional[datetime] = None
        self.steps_executed = 0
        self.steps_total = 0
        self.screenshots: List[str] = []

    @property
    def duration(self) -> float:
        """Return test duration in seconds."""
        if self.start_time and self.end_time:
            return (self.end_time - self.start_time).total_seconds()
        return 0.0

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for reporting."""
        return {
            'script_name': self.script_name,
            'passed': self.passed,
            'error': self.error,
            'duration': self.duration,
            'steps_executed': self.steps_executed,
            'steps_total': self.steps_total,
            'screenshots': self.screenshots,
        }


class BrowserEngine:
    """Executes browser automation tests using Playwright."""

    def __init__(self, headless: bool = True, browser_type: str = 'chromium'):
        """
        Initialize browser engine.

        Args:
            headless: Run browser in headless mode
            browser_type: Browser to use ('chromium', 'firefox', 'webkit')
        """
        self.headless = headless
        self.browser_type = browser_type
        self.browser: Optional[Browser] = None
        self.context: Optional[BrowserContext] = None
        self.page: Optional[Page] = None
        self.actions: Optional[BrowserActions] = None

    async def __aenter__(self):
        """Async context manager entry."""
        await self.start()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit."""
        await self.stop()

    async def start(self) -> None:
        """Start browser instance."""
        self.playwright = await async_playwright().start()

        if self.browser_type == 'chromium':
            self.browser = await self.playwright.chromium.launch(headless=self.headless)
        elif self.browser_type == 'firefox':
            self.browser = await self.playwright.firefox.launch(headless=self.headless)
        elif self.browser_type == 'webkit':
            self.browser = await self.playwright.webkit.launch(headless=self.headless)
        else:
            raise ValueError(f"Unknown browser type: {self.browser_type}")

        self.context = await self.browser.new_context()
        self.page = await self.context.new_page()
        self.actions = BrowserActions(self.page)

    async def stop(self) -> None:
        """Stop browser instance."""
        if self.context:
            await self.context.close()
        if self.browser:
            await self.browser.close()
        if hasattr(self, 'playwright'):
            await self.playwright.stop()

    async def execute_script(self, script: TestScript) -> TestResult:
        """
        Execute a test script.

        Args:
            script: TestScript to execute

        Returns:
            TestResult with execution results
        """
        result = TestResult(script.name)
        result.start_time = datetime.now()
        result.steps_total = len(script.steps)

        try:
            # Set default timeout
            self.page.set_default_timeout(script.timeout)

            # Execute each step
            for i, step in enumerate(script.steps, 1):
                try:
                    print(f"  Step {i}/{len(script.steps)}: {step.action} {step.params}")
                    await self.actions.execute_action(step.action, step.params)
                    result.steps_executed += 1
                except Exception as e:
                    error_msg = f"Step {i} failed ({step.action}): {str(e)}"
                    print(f"  ERROR: {error_msg}")
                    result.error = error_msg

                    if script.screenshot_on_failure:
                        screenshot_path = f"failure_{script.name.replace(' ', '_')}_{i}.png"
                        await self.page.screenshot(path=screenshot_path)
                        result.screenshots.append(screenshot_path)
                        print(f"  Screenshot saved: {screenshot_path}")

                    raise

            result.passed = True
            print(f"  ✓ Test passed: {script.name}")

        except Exception as e:
            result.passed = False
            if not result.error:
                result.error = str(e)
            print(f"  ✗ Test failed: {script.name}")

        finally:
            result.end_time = datetime.now()

        return result

    async def run_test_file(self, script_path: str) -> TestResult:
        """
        Load and execute a test script from file.

        Args:
            script_path: Path to YAML test script

        Returns:
            TestResult
        """
        from ..parser.script_parser import ScriptParser

        print(f"\nLoading test script: {script_path}")
        script = ScriptParser.parse_file(script_path)

        print(f"Validating script...")
        errors = ScriptParser.validate_script(script)
        if errors:
            raise ValueError(f"Script validation failed:\n" + "\n".join(f"  - {e}" for e in errors))

        print(f"Running test: {script.name}")
        print(f"Description: {script.description}")
        print(f"Steps: {len(script.steps)}")

        # Override headless setting from script
        if not self.browser or script.headless != self.headless:
            if self.browser:
                await self.stop()
            self.headless = script.headless
            await self.start()

        return await self.execute_script(script)
