from selenium import webdriver
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
import time
import textwrap

# Initialize the Chrome browser
browser = webdriver.Chrome()

# Open the specified URL
browser.get("https://ru.wikipedia.org/wiki/Заглавная_страница")

# Verify that the page title contains "RoRo - Vessel Schedule"
assert "Википедия" in browser.title


def search_word():
    word = input("Введите слово для поиска в википедии: ")
    search_box = browser.find_element(By.ID, "searchInput")
    search_box.send_keys(word)
    search_box.send_keys(Keys.ENTER)
    word_link = browser.find_element(By.LINK_TEXT, word)
    word_link.click()


def read_paragraph():
    paragraphs = browser.find_elements(By.TAG_NAME, "p")
    quit_word = ''
    for item in paragraphs:
        if quit_word == 'q':
            return
        wrapped_text = textwrap.fill(item.text, width=100)
        print(wrapped_text)
        quit_word = input("Нажмите Enter для продолжения или 'q' для выхода: ")

def all_article_links():
    hatnotes = []
    for element in browser.find_elements(By.TAG_NAME, "div"):
    # Чтобы искать атрибут класса
        cl = element.get_attribute("class")
        if cl == "hatnote navigation-not-searchable":
            hatnotes.append(element)


search_word()
read_paragraph()
# Pause to allow the search results to load


# Optional: Close the browser
browser.quit()
