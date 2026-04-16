from pathlib import Path
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


def create_driver(download_dir="downloads"):
    download_path = str(Path(download_dir).resolve())
    Path(download_path).mkdir(parents=True, exist_ok=True)

    chrome_options = Options()
    chrome_options.add_experimental_option("prefs", {
        "download.default_directory": download_path,
        "download.prompt_for_download": False,
        "download.directory_upgrade": True,
        "safebrowsing.enabled": True
    })

    driver = webdriver.Chrome(options=chrome_options)
    driver.maximize_window()
    return driver