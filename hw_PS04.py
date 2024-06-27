from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By


def initialize_driver():
    geckodriver_path = 'C:/Users/geckodriver/geckodriver.exe'
    service = Service(geckodriver_path)
    options = Options()
    options.headless = True
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    options.add_argument('--window-size=1920,1080')
    driver = webdriver.Firefox(service=service, options=options)
    return driver


def search_wikipedia(driver, query):
    url = f"https://ru.wikipedia.org/wiki/{query.replace(' ', '_')}"
    driver.get(url)
    if "Википедия не имеет статьи с таким названием" in driver.page_source:
        return None
    return driver


def list_paragraphs(driver):
    paragraphs = driver.find_elements(By.CSS_SELECTOR, "p")
    for para in paragraphs:
        print(para.text[:500] + '...')  # выводим только первые 500 символов текста параграфа
        input("Нажмите Enter для продолжения...\n")


def list_links(driver):
    links = []
    for element in driver.find_elements(By.TAG_NAME, "div"):
        cl = element.get_attribute("class")
        if cl == "hatnote navigation-not-searchable":
            links.append(element)

    for link in links:
        print(link.text)


def main():
    driver = initialize_driver()

    query = input("Введите запрос: ")

    driver = search_wikipedia(driver, query)
    if not driver:
        print("Страница не найдена.")
        return

    while True:
        print("\nВыберите действие:")
        print("1. Листать параграфы текущей статьи")
        print("2. Перейти на одну из связанных страниц")
        print("3. Выйти из программы")
        choice = input("Введите номер действия: ")

        if choice == '1':
            list_paragraphs(driver)
        elif choice == '2':
            print("Связанные страницы:")
            list_links(driver)
            new_query = input("Введите название связанной страницы: ")
            driver = search_wikipedia(driver, new_query)
            if not driver:
                print("Страница не найдена.")
                return
        elif choice == '3':
            print("Выход из программы.")
            break
        else:
            print("Неправильный выбор. Пожалуйста, попробуйте снова.")

    driver.quit()


if __name__ == "__main__":
    main()
