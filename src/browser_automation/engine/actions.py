"""Browser action implementations using Playwright."""
from typing import Any, Dict
from pathlib import Path
from playwright.async_api import Page, expect


class BrowserActions:
    """Handles browser automation actions."""

    def __init__(self, page: Page):
        self.page = page

    async def navigate(self, url: str, **kwargs) -> None:
        """Navigate to URL."""
        await self.page.goto(url, **kwargs)

    async def click(self, selector: str, **kwargs) -> None:
        """Click an element."""
        await self.page.click(selector, **kwargs)

    async def type(self, selector: str, text: str, **kwargs) -> None:
        """Type text into an element."""
        await self.page.fill(selector, text, **kwargs)

    async def wait_for_selector(self, selector: str, timeout: int = 30000, **kwargs) -> None:
        """Wait for selector to appear."""
        await self.page.wait_for_selector(selector, timeout=timeout, **kwargs)

    async def assert_text(self, selector: str, expected: str, **kwargs) -> None:
        """Assert element contains expected text."""
        element = self.page.locator(selector)
        await expect(element).to_contain_text(expected, **kwargs)

    async def assert_visible(self, selector: str, **kwargs) -> None:
        """Assert element is visible."""
        element = self.page.locator(selector)
        await expect(element).to_be_visible(**kwargs)

    async def upload_file(self, selector: str, file_path: str, **kwargs) -> None:
        """Upload a file."""
        path = Path(file_path).expanduser()
        if not path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")
        await self.page.set_input_files(selector, str(path.absolute()), **kwargs)

    async def screenshot(self, filename: str, **kwargs) -> None:
        """Take a screenshot."""
        await self.page.screenshot(path=filename, **kwargs)

    async def wait(self, ms: int, **kwargs) -> None:
        """Wait for specified milliseconds."""
        await self.page.wait_for_timeout(ms)

    async def select_option(self, selector: str, value: str, **kwargs) -> None:
        """Select option from dropdown."""
        await self.page.select_option(selector, value, **kwargs)

    async def check(self, selector: str, **kwargs) -> None:
        """Check a checkbox."""
        await self.page.check(selector, **kwargs)

    async def uncheck(self, selector: str, **kwargs) -> None:
        """Uncheck a checkbox."""
        await self.page.uncheck(selector, **kwargs)

    async def hover(self, selector: str, **kwargs) -> None:
        """Hover over an element."""
        await self.page.hover(selector, **kwargs)

    async def press(self, selector: str, key: str, **kwargs) -> None:
        """Press a key on an element."""
        await self.page.press(selector, key, **kwargs)

    async def evaluate_js(self, script: str, **kwargs) -> Any:
        """Execute JavaScript and return the result."""
        result = await self.page.evaluate(script, **kwargs)
        print(f"  JavaScript result: {result}")
        return result

    async def count_elements(self, selector: str, **kwargs) -> None:
        """Count elements matching selector and log the count."""
        count = await self.page.locator(selector).count()
        print(f"  Found {count} elements matching '{selector}'")
        if count == 0:
            raise AssertionError(f"Expected at least 1 element matching '{selector}', found 0")

    async def assert_count(self, selector: str, expected: int, **kwargs) -> None:
        """Assert specific count of elements."""
        count = await self.page.locator(selector).count()
        print(f"  Found {count} elements matching '{selector}' (expected {expected})")
        if count != expected:
            raise AssertionError(f"Expected {expected} elements matching '{selector}', found {count}")

    async def assert_min_count(self, selector: str, minimum: int, **kwargs) -> None:
        """Assert minimum count of elements."""
        count = await self.page.locator(selector).count()
        print(f"  Found {count} elements matching '{selector}' (minimum {minimum})")
        if count < minimum:
            raise AssertionError(f"Expected at least {minimum} elements matching '{selector}', found {count}")

    async def get_text(self, selector: str, **kwargs) -> None:
        """Get text content of element and log it."""
        element = self.page.locator(selector)
        text = await element.text_content()
        print(f"  Text from '{selector}': {text}")

    async def execute_action(self, action: str, params: Dict[str, Any]) -> None:
        """
        Execute a browser action by name.

        Args:
            action: Action name (e.g., 'click', 'type')
            params: Action parameters

        Raises:
            ValueError: If action is unknown
        """
        method = getattr(self, action, None)
        if method is None:
            raise ValueError(f"Unknown action: {action}")

        await method(**params)
