from pathlib import Path
from urllib.request import urlretrieve
import zipfile

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from browser import create_driver


BASE_URL = "https://rpachallenge.com/"
INVOICE_URL_PART = "rpachallengeocr.azurewebsites.net"
DOWNLOAD_DIR = Path("downloads")
OUTPUT_DIR = Path("output")
ZIP_PATH = OUTPUT_DIR / "invoices_2_4.zip"

TARGET_INVOICES = {2, 4}


def log(message):
    print(message)


def ensure_directories():
    DOWNLOAD_DIR.mkdir(parents=True, exist_ok=True)
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


def clear_previous_files():
    for file_path in DOWNLOAD_DIR.glob("invoice_*.jpg"):
        file_path.unlink(missing_ok=True)

    if ZIP_PATH.exists():
        ZIP_PATH.unlink()


def open_invoice_extraction(driver, wait):
    log("Abrindo site principal...")
    driver.get(BASE_URL)

    invoice_tab = wait.until(
        EC.element_to_be_clickable(
            (By.XPATH, "//a[contains(@href, 'rpachallengeocr.azurewebsites.net')]")
        )
    )

    log("Clicando na aba Invoice Extraction...")
    try:
        invoice_tab.click()
    except Exception:
        driver.execute_script("arguments[0].click();", invoice_tab)

    wait.until(lambda d: INVOICE_URL_PART in d.current_url)
    log(f"Página de invoice aberta: {driver.current_url}")


def wait_for_invoice_table(driver, wait):
    log("Aguardando tabela de invoices carregar...")

    wait.until(EC.presence_of_element_located((By.ID, "tableSandbox")))
    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "#tableSandbox tbody")))
    wait.until(lambda d: len(d.find_elements(By.CSS_SELECTOR, "#tableSandbox tbody tr")) > 0)

    log("Tabela carregada com linhas.")


def wait_for_target_invoices(driver, wait, target_invoices):
    log(f"Aguardando invoices {sorted(target_invoices)} aparecerem na tabela...")

    def invoices_loaded(d):
        rows = d.find_elements(By.CSS_SELECTOR, "#tableSandbox tbody tr")
        found = set()

        for row in rows:
            cols = row.find_elements(By.TAG_NAME, "td")
            if not cols:
                continue

            first_col = cols[0].text.strip()
            if first_col.isdigit():
                found.add(int(first_col))

        return target_invoices.issubset(found)

    wait.until(invoices_loaded)
    log("Invoices alvo encontrados na tabela.")


def read_invoice_table(driver):
    rows = driver.find_elements(By.CSS_SELECTOR, "#tableSandbox tbody tr")
    log(f"Linhas encontradas na tabela: {len(rows)}")

    invoice_links = {}

    for row in rows:
        cols = row.find_elements(By.TAG_NAME, "td")
        if len(cols) < 4:
            continue

        invoice_number_text = cols[0].text.strip()

        if not invoice_number_text.isdigit():
            continue

        invoice_number = int(invoice_number_text)

        if invoice_number not in TARGET_INVOICES:
            continue

        link_element = cols[3].find_element(By.TAG_NAME, "a")
        href = link_element.get_attribute("href")

        if href:
            invoice_links[invoice_number] = href
            log(f"Invoice {invoice_number} -> {href}")

    return invoice_links


def download_invoices(invoice_links):
    downloaded_files = []

    for invoice_number in sorted(invoice_links.keys()):
        url = invoice_links[invoice_number]
        destination = DOWNLOAD_DIR / f"invoice_{invoice_number}.jpg"

        log(f"Baixando invoice {invoice_number}...")
        urlretrieve(url, destination)

        if not destination.exists():
            raise FileNotFoundError(f"Falha ao baixar invoice {invoice_number}")

        downloaded_files.append(destination)
        log(f"Arquivo salvo em: {destination}")

    return downloaded_files


def create_zip(files):
    log(f"Criando ZIP: {ZIP_PATH}")

    with zipfile.ZipFile(ZIP_PATH, "w", zipfile.ZIP_DEFLATED) as zip_file:
        for file_path in files:
            zip_file.write(file_path, arcname=file_path.name)

    if not ZIP_PATH.exists():
        raise FileNotFoundError("Falha ao criar o arquivo ZIP.")

    log(f"ZIP criado com sucesso: {ZIP_PATH}")


def extract_and_zip_invoices():
    ensure_directories()
    clear_previous_files()

    driver = create_driver(download_dir=str(DOWNLOAD_DIR))
    wait = WebDriverWait(driver, 20)

    try:
        open_invoice_extraction(driver, wait)
        wait_for_invoice_table(driver, wait)
        wait_for_target_invoices(driver, wait, TARGET_INVOICES)

        invoice_links = read_invoice_table(driver)

        missing = TARGET_INVOICES - set(invoice_links.keys())
        if missing:
            raise Exception(f"Não foi possível localizar os invoices: {sorted(missing)}")

        downloaded_files = download_invoices(invoice_links)
        create_zip(downloaded_files)

        log("Processo finalizado com sucesso.")
        log(f"Arquivos baixados: {[file.name for file in downloaded_files]}")
        log(f"ZIP final: {ZIP_PATH}")

    finally:
        driver.quit()


if __name__ == "__main__":
    extract_and_zip_invoices()