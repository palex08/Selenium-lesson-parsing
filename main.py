from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import textwrap
import time


def initialize_browser():
    browser = webdriver.Chrome()
    browser.get("https://ru.wikipedia.org/wiki/Заглавная_страница")
    assert "Википедия" in browser.title
    return browser


def search_word(browser, word):
    search_box = browser.find_element(By.ID, "searchInput")
    search_box.send_keys(word)
    search_box.send_keys(Keys.ENTER)
    word_link = browser.find_element(By.LINK_TEXT, word)
    word_link.click()


def read_paragraph(browser):
    paragraphs = browser.find_elements(By.TAG_NAME, "p")
    for item in paragraphs:
        wrapped_text = textwrap.fill(item.text, width=100)
        print(wrapped_text)
        user_input = input("Нажмите Enter для продолжения или 'q' для выхода: ")
        if user_input.lower() == 'q':
            break


def get_internal_links(browser):
    links = browser.find_elements(By.XPATH, "//div[@class='hatnote navigation-not-searchable']//a[@href]")
    internal_links = [link for link in links if '/wiki/' in link.get_attribute('href')]
    return internal_links


def navigate_to_internal_link(links):
    for idx, link in enumerate(links[:10]):  # Display only first 10 links
        print(f"{idx + 1}. {link.text}")
    choice = int(input("Выберите номер ссылки для перехода или 0 для отмены: "))
    if 1 <= choice <= len(links[:10]):
        links[choice - 1].click()
        time.sleep(2)  # Wait for the page to load


def main():
    browser = initialize_browser()
    try:
        initial_word = input("Введите слово для поиска в Википедии: ")
        search_word(browser, initial_word)

        while True:
            print("\nВыберите действие:")
            print("1. Листать параграфы текущей статьи")
            print("2. Перейти на одну из связанных страниц")
            print("3. Выйти из программы")
            choice = input("Ваш выбор: ")

            if choice == '1':
                read_paragraph(browser)
            elif choice == '2':
                internal_links = get_internal_links(browser)
                if internal_links:
                    navigate_to_internal_link(internal_links)
                else:
                    print("Внутренние ссылки не найдены.")
            elif choice == '3':
                print("Выход из программы.")
                break
            else:
                print("Неверный выбор. Попробуйте снова.")
    finally:
        browser.quit()


if __name__ == "__main__":
    main()
