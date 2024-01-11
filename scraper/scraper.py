from bs4 import BeautifulSoup
from os import path
import csv
from config import TECH_STACK, URL

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from config import GRADES
from scraper.driver import ChromeDriver


def is_paginated(driver):
    try:
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR,
                    "ul.pagination.pagination_with_numbers >"
                    " li.page-item.active > span.page-link")
            )
        )
        return True
    except TimeoutException:
        return False


def is_pagination_present(driver, url):
    if is_paginated(driver):
        buttons_menu = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.CLASS_NAME, "page-link"))
        )
        if not buttons_menu[-1].get_attribute("aria-disabled"):
            buttons_menu[-1].click()
            print(f"click on page {driver.current_url}")
            WebDriverWait(driver, 10).until(EC.url_changes(url))
            return True
    return False


def get_next_page(driver, url):
    if is_pagination_present(driver, url):
        return driver.current_url
    return False


def parse_page(driver: ChromeDriver, url):
    driver.get(url)
    vacancies_soup = BeautifulSoup(driver.page_source, "html.parser"
                                   ).find_all("div",
                                              class_="job-list-item position-relative")
    vacancies = []
    for vacancy_soup in vacancies_soup:
        vacancies.append(f"{parse_single_vacancy(vacancy_soup)}")
    return vacancies


def parse_single_vacancy(vacancy_soup):
    soup = vacancy_soup.select_one("div.job-list-item__description > span")["data-original-text"]
    technology_counts = [tech for tech in TECH_STACK if tech.lower() in soup.lower()]
    return technology_counts


def parse_all_pages(driver: ChromeDriver, start_url):
    current_url = start_url
    all_vacancies = []

    while current_url:
        driver.get(current_url)
        vacancies_on_page = parse_page(driver, current_url)
        all_vacancies.extend(vacancies_on_page)

        current_url = get_next_page(driver, current_url)
    return all_vacancies


def parse_by_grade(driver: ChromeDriver, url, grade):
    driver.get(url)
    if grade != "general":
        label = driver.find_element(By.CSS_SELECTOR, f"label[for='exp_rank_{grade}']")
        label.click()
    return parse_all_pages(driver, driver.current_url)


def write_to_csv(driver, url, grades):
    for grade in grades:
        data = parse_by_grade(driver, url, grade)
        with open(path.join("raw_data", f"{grade}.csv"), "a", encoding="utf8", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["tech_stack"])
            writer.writerows([[d] for d in data])


if __name__ == "__main__":
    with ChromeDriver() as driver:
        write_to_csv(driver, URL, GRADES)
