import pytest
import json
from pathlib import Path
from playwright.sync_api import sync_playwright
from playwright.sync_api import Browser, BrowserContext, Page
from nopcommerce.src.pages.LoginPage import LoginPage
import pyautogui
import pygetwindow as gw

# Add a command-line option for browser type
def pytest_addoption(parser):
    parser.addoption("--browser-type", action="store", default="chromium", help="Specify the browser type: chromium, firefox, webkit")

# Fixture to get the browser type
@pytest.fixture()
def browser_type(request, config_data):
    # Use the value passed through the command-line option, or default to "chromium"
    selected_browser = request.config.getoption("--browser-type") or config_data["default_browser"]
    print(f"Selected browser: {selected_browser}")
    return selected_browser



# Fixture to set up and tear down the test
@pytest.fixture()
def set_up_tear_down(page: Page, config_data, browser_type) -> None:
    page.goto(config_data["url"])
    yield page

# Fixture to create a browser context
@pytest.fixture()
def browser_context(playwright, browser_type, config_data):
    browser_config = config_data["browsers"].get(browser_type, {})
    return playwright[browser_config["type"]].launch(headless=browser_config["headless"])

# Fixture to create a new page
@pytest.fixture()
def page(browser_context):
    return browser_context.new_page()

# Fixture to get configuration data
@pytest.fixture()
def config_data():
    # Get the directory of the current script
    script_directory = Path(__file__).resolve().parent

    # Move up to the project directory and then descend into src/Testdata
    config_path = script_directory.parent / "src" / "Testdata" / "config.json"

    with open(config_path) as f:
        return json.load(f)

# Fixture to get browser configuration data
@pytest.fixture()
def browsers_config():
    # Get the directory of the current script
    script_directory = Path(__file__).resolve().parent

    # Move up to the project directory and then descend into src/Testdata
    browsers_config_path = script_directory.parent / "src" / "Testdata" / "browsers.json"

    with open(browsers_config_path) as f:
        return json.load(f)

# Fixture to log in to the application
@pytest.fixture()
def login_to_app(page, config_data):
    login_page = LoginPage(page)
    return login_page.do_login(config_data["credentials"])


@pytest.fixture()
def video_recording(request):
    # Set up the video recorder using pygetwindow and pyautogui
    screen = gw.getWindowsWithTitle("Your Application Title")[0]  # Replace with your application title
    screen_rect = screen._rect
    video_recorder = pyautogui.screenshot(
        region=(screen_rect.left, screen_rect.top, screen_rect.width, screen_rect.height))

    # Get the path to the framework directory
    framework_path = Path(__file__).resolve().parent.parent  # Assumes conftest.py is at the root of your framework

    # Add a finalizer to stop recording after the test
    def finalize():
        # Construct the absolute path to save the recorded video (adjust the path accordingly)
        video_path = framework_path / "videos" / "recorded_video.mp4"

        # Save the recorded video
        video_recorder.save(str(video_path))

        # Optionally, you can perform additional actions such as moving the video file

    request.addfinalizer(finalize)

    return video_recorder