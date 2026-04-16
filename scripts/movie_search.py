from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, ElementClickInterceptedException

from browser import create_driver
from db import create_table, insert_movie, movie_exists


URL = "https://rpachallenge.com/"
SEARCH_TERM = "Avengers"


def log(message):
    print(message)


def click_movie_search_tab(driver, wait):
    movie_tab = wait.until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "a[href='/movieSearch']"))
    )

    try:
        movie_tab.click()
    except Exception:
        driver.execute_script("arguments[0].click();", movie_tab)

    wait.until(EC.url_contains("/movieSearch"))


def find_search_input(wait):
    return wait.until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, "input[name='searchStr']"))
    )


def find_search_button(wait):
    return wait.until(
        EC.element_to_be_clickable(
            (By.XPATH, "//button[normalize-space()='Find' or normalize-space()='FIND']")
        )
    )


def extract_text_content(driver, element):
    return driver.execute_script("return arguments[0].textContent;", element).strip()


def extract_movies(driver, wait):
    wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "div.cardItem")))

    cards = driver.find_elements(By.CSS_SELECTOR, "div.cardItem")
    movies = []
    seen = set()

    for card in cards:
        title = ""
        description = ""

        try:
            title_el = card.find_element(By.CSS_SELECTOR, "div.card-reveal span.card-title")
            title = extract_text_content(driver, title_el).replace("close", "").strip()
        except Exception:
            pass

        if not title:
            try:
                title_el = card.find_element(By.CSS_SELECTOR, "div.card-content span.card-title.activator")
                title = extract_text_content(driver, title_el)
            except Exception:
                pass

        try:
            description_el = card.find_element(By.CSS_SELECTOR, "div.card-reveal p")
            description = extract_text_content(driver, description_el)
        except Exception:
            pass

        if not description:
            try:
                description_el = card.find_element(By.CSS_SELECTOR, "div.card-content p")
                description = extract_text_content(driver, description_el)
            except Exception:
                pass

        title = " ".join(title.split())
        description = " ".join(description.split())

        if not title or not description:
            continue

        key = (title, description)
        if key not in seen:
            seen.add(key)
            movies.append({
                "movie_name": title,
                "description": description
            })

    return movies


def save_movies_to_db(movies, search_term=SEARCH_TERM):
    saved_count = 0

    for movie in movies:
        if not movie_exists(movie["movie_name"], search_term):
            insert_movie(movie["movie_name"], movie["description"], search_term)
            saved_count += 1

    return saved_count


def search_avengers_and_save():
    create_table()

    driver = create_driver()
    wait = WebDriverWait(driver, 10)

    try:
        log("Abrindo site...")
        driver.get(URL)

        click_movie_search_tab(driver, wait)

        search_input = find_search_input(wait)
        search_input.clear()
        search_input.send_keys(SEARCH_TERM)

        find_button = find_search_button(wait)

        try:
            find_button.click()
        except ElementClickInterceptedException:
            driver.execute_script("arguments[0].click();", find_button)

        movies = extract_movies(driver, wait)

        if not movies:
            log("Nenhum filme encontrado.")
            return

        saved_count = save_movies_to_db(movies, SEARCH_TERM)

        log(f"Filmes encontrados: {len(movies)}")
        log(f"Filmes salvos no banco: {saved_count}")

        for movie in movies:
            print("-" * 60)
            print("Filme:", movie["movie_name"])
            print("Descrição:", movie["description"])

        log("Processo finalizado com sucesso.")

    except TimeoutException as e:
        log(f"TIMEOUT: {e}")

    except Exception as e:
        log(f"ERRO GERAL: {type(e).__name__} - {e}")

    finally:
        driver.quit()


if __name__ == "__main__":
    search_avengers_and_save()