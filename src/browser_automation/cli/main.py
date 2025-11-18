"""CLI interface for browser automation."""
import asyncio
import argparse
import sys
from pathlib import Path
from typing import List

from ..engine.browser_engine import BrowserEngine, TestResult
from ..parser.script_parser import ScriptParser


def print_result(result: TestResult) -> None:
    """Print test result summary."""
    status = "✓ PASSED" if result.passed else "✗ FAILED"
    print(f"\n{'='*60}")
    print(f"Test: {result.script_name}")
    print(f"Status: {status}")
    print(f"Duration: {result.duration:.2f}s")
    print(f"Steps: {result.steps_executed}/{result.steps_total}")

    if result.error:
        print(f"Error: {result.error}")

    if result.screenshots:
        print(f"Screenshots: {', '.join(result.screenshots)}")

    print(f"{'='*60}\n")


async def run_tests(script_paths: List[str], headless: bool, browser: str) -> int:
    """
    Run test scripts.

    Args:
        script_paths: List of test script paths
        headless: Run in headless mode
        browser: Browser type

    Returns:
        Exit code (0 for success, 1 for failure)
    """
    results = []

    async with BrowserEngine(headless=headless, browser_type=browser) as engine:
        for script_path in script_paths:
            try:
                result = await engine.run_test_file(script_path)
                results.append(result)
                print_result(result)
            except Exception as e:
                print(f"\n✗ Failed to run {script_path}: {e}\n")
                results.append(TestResult(script_path))
                results[-1].error = str(e)

    # Summary
    passed = sum(1 for r in results if r.passed)
    failed = len(results) - passed

    print(f"\n{'='*60}")
    print(f"SUMMARY: {passed} passed, {failed} failed out of {len(results)} tests")
    print(f"{'='*60}\n")

    return 0 if failed == 0 else 1


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description="NexusRAG Browser Automation Tool",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Run single test in headed mode
  uv run python -m browser_automation.cli.main test_scripts/upload.yaml --headed

  # Run multiple tests in headless mode
  uv run python -m browser_automation.cli.main test_scripts/*.yaml

  # Run with Firefox
  uv run python -m browser_automation.cli.main test_scripts/search.yaml --browser firefox

  # Validate a test script
  uv run python -m browser_automation.cli.main --validate test_scripts/upload.yaml
        """
    )

    parser.add_argument(
        'scripts',
        nargs='+',
        help='Test script file(s) to run'
    )

    parser.add_argument(
        '--headless',
        action='store_true',
        default=True,
        help='Run in headless mode (default)'
    )

    parser.add_argument(
        '--headed',
        action='store_true',
        help='Run in headed mode (show browser)'
    )

    parser.add_argument(
        '--browser',
        choices=['chromium', 'firefox', 'webkit'],
        default='chromium',
        help='Browser to use (default: chromium)'
    )

    parser.add_argument(
        '--validate',
        action='store_true',
        help='Only validate scripts without running them'
    )

    args = parser.parse_args()

    # Validate mode
    if args.validate:
        all_valid = True
        for script_path in args.scripts:
            try:
                print(f"\nValidating: {script_path}")
                script = ScriptParser.parse_file(script_path)
                errors = ScriptParser.validate_script(script)

                if errors:
                    print(f"✗ Validation failed:")
                    for error in errors:
                        print(f"  - {error}")
                    all_valid = False
                else:
                    print(f"✓ Valid script: {script.name}")
                    print(f"  Steps: {len(script.steps)}")

            except Exception as e:
                print(f"✗ Error: {e}")
                all_valid = False

        return 0 if all_valid else 1

    # Run mode
    headless = not args.headed if args.headed else args.headless

    try:
        exit_code = asyncio.run(run_tests(args.scripts, headless, args.browser))
        sys.exit(exit_code)
    except KeyboardInterrupt:
        print("\n\nInterrupted by user")
        sys.exit(130)


if __name__ == '__main__':
    main()
