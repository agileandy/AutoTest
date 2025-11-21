# AutoTest - Browser Automation Testing Framework

A Playwright-based browser automation testing framework that reads YAML test scripts and executes them against web applications.

This is one of two different ideas I'm working on to build 'intelligent' AI based testing tools.   The other is https://github.com/agileandy/AutoPilot-Forge. Both are very much early WIP at the moment.

## Features

- **YAML-based test scripts** - Write tests in simple, declarative format
- **Playwright integration** - Chromium, Firefox, WebKit support
- **Headed/headless modes** - Run with visible browser or in background
- **19 browser actions** - Navigate, click, type, upload, assert, and more
- **Screenshot on failure** - Automatic debugging screenshots
- **Test validation** - Validate scripts without running them
- **Element counting** - Verify table rows, list items, etc.
- **JavaScript evaluation** - Execute custom scripts in browser

## Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/AutoTest.git
cd AutoTest

# Install dependencies (requires uv)
uv pip install playwright pytest-playwright pyyaml pytest-asyncio

# Install browser binaries
uv run playwright install chromium
```

## Quick Start

### Run a test in headed mode (see browser)

```bash
uv run python -m browser_automation.cli.main test_scripts/example_test.yaml --headed
```

### Run in headless mode

```bash
uv run python -m browser_automation.cli.main test_scripts/example_test.yaml
```

### Validate a test script

```bash
uv run python -m browser_automation.cli.main --validate test_scripts/example_test.yaml
```

## Test Script Format

```yaml
name: "My Test"
description: "What this test does"
base_url: "http://localhost:8000"
headless: false
timeout: 60000

steps:
  - action: navigate
    url: "http://localhost:8000/"

  - action: type
    selector: "#username"
    text: "admin"

  - action: click
    selector: "#submit-btn"

  - action: assert_text
    selector: ".welcome"
    expected: "Welcome"

  - action: screenshot
    filename: "result.png"
```

## Available Actions

### Navigation & Waiting
- `navigate` - Navigate to URL
- `wait_for_selector` - Wait for element
- `wait` - Wait milliseconds

### Interaction
- `click` - Click element
- `type` - Type text
- `upload_file` - Upload file
- `select_option` - Select dropdown
- `check` / `uncheck` - Checkbox
- `hover` - Hover element
- `press` - Press key

### Assertions
- `assert_text` - Assert text content
- `assert_visible` - Assert visibility
- `assert_count` - Assert exact count
- `assert_min_count` - Assert minimum count

### Debugging
- `screenshot` - Capture screenshot
- `count_elements` - Count and log
- `get_text` - Get and log text
- `evaluate_js` - Run JavaScript

## Project Structure

```
AutoTest/
├── src/browser_automation/
│   ├── parser/          # YAML parsing
│   ├── engine/          # Playwright automation
│   └── cli/             # CLI interface
├── test_scripts/        # Your test files
└── README.md
```

## CLI Options

```bash
uv run python -m browser_automation.cli.main [OPTIONS] SCRIPTS...

Options:
  --headed      Show browser
  --headless    Background (default)
  --browser     chromium/firefox/webkit
  --validate    Check scripts only
```

## License

MIT License
