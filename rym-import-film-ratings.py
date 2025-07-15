import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver import ActionChains
#import pyperclip
import csv
import time

def duckduckgo_first_result(driver, film, year, max_attempts = 3):
    for i in range(1, max_attempts + 1):
        try:
            wait_for_searchbox = WebDriverWait(driver, 5)
            wait_for_js = WebDriverWait(driver, 2)
            driver.get("https://duckduckgo.com")
            # Wait for search box and type query
            search_box = wait_for_searchbox.until(
                EC.presence_of_element_located((By.ID, "searchbox_input"))
            )
            query = f"\\{film} {year} site:rateyourmusic.com/film"
            search_box.clear()
            # Set form (in this case, search bar) value using JS...
            driver.execute_script("arguments[0].value = arguments[1];", search_box, query)
            # ...then submit
            driver.execute_script("arguments[0].form.submit();", search_box)
            wait_for_js.until(EC.url_contains("rateyourmusic.com/film"))
            return
        except Exception:
            print(f"Hubo un problema buscando la pelicula {film} ({year}). Intento {i}/{max_attempts}.")
            continue
    raise Exception("Error en DuckDuckGo")

def read_letterboxd_csv(csv_path):
    with open(csv_path, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        return list(reader)

def set_rym_rating(driver, rating):
    # Convert rating from /5 to /10 scale
    rating_10 = float(rating) * 2
    wait = WebDriverWait(driver, 5)
    # Find the rating element
    rating_div = wait.until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "div[id^='rating_stars_F_']"))
    )
    # Get the element's width to calculate position
    width = rating_div.size['width']
    # Calculate x position (rating_10 * width / 10)
    # offset is calculated from the center point of the div
    x_offset = (rating_10 * width / 10.0) - width / 2.0
    # Use ActionChains to move and click
    actions = ActionChains(driver)
    actions.move_to_element_with_offset(rating_div, x_offset, 0)
    actions.click()
    actions.perform()
    # Wait a moment for the rating to be saved
    time.sleep(1)


if __name__ == "__main__":
    driver = uc.Chrome(headless=False, use_subprocess=False, enable_cdp_events=True)
    driver.get("https://rateyourmusic.com/account/login")
    input("Logeate en rateyourmusic y presiona ENTER.")
    ratings = read_letterboxd_csv("./data/ratings.csv")  # Update path as needed
    for entry in ratings[235:]:
        film_name = entry['Name']
        year = entry['Year']
        rating = entry['Rating']
        try:
            duckduckgo_first_result(driver, film_name, year)
            set_rym_rating(driver, rating)
        except Exception:
            print(f"!! La pelicula {film_name} ({year}) no pudo ser puntuada.")
    driver.quit()