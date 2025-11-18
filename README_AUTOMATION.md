# NexusRAG Browser Automation Tool

Successfully created and tested browser-based automation tool for NexusRAG using Playwright.

## What Was Built

A complete Playwright-based browser automation framework with:

- **YAML-based test scripts**: Easy-to-write declarative test definitions
- **Full browser control**: Navigate, click, type, upload files, take screenshots, assertions
- **Headed/headless modes**: Run with visible browser or in background
- **Multi-browser support**: Chromium, Firefox, WebKit
- **CLI interface**: Simple command-line tool for running tests
- **Screenshot on failure**: Automatic debugging screenshots
- **Test validation**: Validate scripts without running them

## Installation

Dependencies are already installed in this worktree:
- playwright
- pytest-playwright
- pyyaml
- pytest-asyncio

Chromium browser is installed and ready.

## Test Results

Successfully ran first automation test:

**Test**: Upload AI Ebook to NexusRAG
- **Status**: ✓ PASSED
- **Duration**: 40.98 seconds
- **Steps Completed**: 11/11
- **Document Uploaded**: "Agents in the Long Game of AI..." (AI textbook PDF)

Screenshots captured:
- `nexusrag_before_upload.png` (55K) - Initial UI state
- `nexusrag_during_upload.png` (57K) - Upload in progress
- `nexusrag_after_upload.png` (99K) - After successful upload

## Usage

### Run a Test

```bash
# Headed mode (see browser)
uv run python -m browser_automation.cli.main test_scripts/upload_ai_ebook.yaml --headed

# Headless mode (background)
uv run python -m browser_automation.cli.main test_scripts/upload_ai_ebook.yaml

# Use Firefox
uv run python -m browser_automation.cli.main test_scripts/upload_ai_ebook.yaml --browser firefox --headed
```

### Validate a Test Script

```bash
uv run python -m browser_automation.cli.main --validate test_scripts/upload_ai_ebook.yaml
```

### Run Multiple Tests

```bash
uv run python -m browser_automation.cli.main test_scripts/*.yaml
```

## Test Script Format

Tests are written in YAML:

```yaml
name: "Test Name"
description: "What this test does"
base_url: "http://localhost:8000"
headless: false
timeout: 120000

steps:
  - action: navigate
    url: "http://localhost:8000/"

  - action: wait_for_selector
    selector: "#uploadArea"

  - action: upload_file
    selector: "#fileInput"
    file_path: "~/ebooks/ai/sample.pdf"

  - action: screenshot
    filename: "result.png"

  - action: assert_visible
    selector: "#documentTitle"
```

## Available Actions

| Action | Parameters | Description |
|--------|-----------|-------------|
| `navigate` | `url` | Navigate to URL |
| `click` | `selector` | Click element |
| `type` | `selector`, `text` | Type text into input |
| `wait_for_selector` | `selector`, `timeout` | Wait for element to appear |
| `assert_text` | `selector`, `expected` | Assert element contains text |
| `assert_visible` | `selector` | Assert element is visible |
| `upload_file` | `selector`, `file_path` | Upload file to input (supports ~/) |
| `screenshot` | `filename` | Take screenshot |
| `wait` | `ms` | Wait for milliseconds |
| `select_option` | `selector`, `value` | Select dropdown option |
| `check` | `selector` | Check checkbox |
| `uncheck` | `selector` | Uncheck checkbox |
| `hover` | `selector` | Hover over element |
| `press` | `selector`, `key` | Press key on element |

## Architecture

```
src/browser_automation/
├── parser/           # YAML script parsing and validation
│   └── script_parser.py
├── engine/           # Playwright automation engine
│   ├── browser_engine.py  # Test execution
│   └── actions.py         # Browser action implementations
└── cli/              # Command-line interface
    └── main.py

test_scripts/         # YAML test definitions
examples/             # Example test files
tests/                # Unit and integration tests
```

## Example Test Scripts

### Upload AI Ebook
Located at: `test_scripts/upload_ai_ebook.yaml`

This test:
1. Opens nexusRAG in browser
2. Waits for UI to load
3. Uploads an AI textbook PDF
4. Waits for processing to complete
5. Takes screenshots at each stage
6. Verifies upload success

## Next Steps

Potential enhancements:
- Add more test scripts for different workflows
- Implement search testing
- Add job log verification tests
- Create database admin tests
- Add parallel test execution
- Generate HTML test reports
- Add video recording for tests
- Create CI/CD integration examples

## Development Notes

This browser automation tool was created in an independent git worktree on branch `feat/browser-automation-testing`. It uses:

- **TDD approach**: Test-driven development
- **Playwright**: Modern, reliable browser automation
- **Python async/await**: Efficient concurrent execution
- **YAML**: Human-readable test definitions
- **CLI-first**: Easy to integrate into scripts and CI/CD

The tool successfully automated document upload to nexusRAG, demonstrating end-to-end browser control and validation capabilities.
