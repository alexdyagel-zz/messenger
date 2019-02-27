#!/usr/bin/env python3
import csv
from bs4 import BeautifulSoup
import requests
from collections import Counter
from string import punctuation


class ProgrammingLanguage:
    def __init__(self, name, rating):
        self.name = name
        self.rating = rating

    def __str__(self):
        return "Programming Language: {}\n Rating: {}".format(self.name, self.rating)


class Scrapper:
    BASE_URL = 'https://www.tiobe.com/tiobe-index/'

    def __init__(self, url=BASE_URL):
        self.url = url
        self.html_page = self.get_html_page()
        self.soup = BeautifulSoup(self.html_page, "html.parser")
        self.languages = []

    def get_html_page(self):
        response = requests.get(self.url)
        return response.text

    def parse_top_programming_languages(self):
        table = self.soup.find('table', class_='table table-striped table-top20')
        rows = table.find_all('tr')[1:]
        for row in rows:
            cols = row.find_all('td')
            _, _, _, language, rating, _ = cols
            language = language.text
            rating = float(rating.text.replace("%", ""))

            self.languages.append(ProgrammingLanguage(language, rating))
        return self.languages

    def get_rating_of_language(self, lang):
        needed_language = next((language for language in self.languages if language.name == lang), None)
        return needed_language.rating if needed_language is not None else None

    def count_words_on_page(self):
        # We get the words in p tags
        text_in_p_blocks_generator = (''.join(p_tag.findAll(text=True)) for p_tag in self.soup.findAll('p'))
        counter_for_p_blocks = Counter(
            (word.rstrip(punctuation).lower() for text_in_single_block in text_in_p_blocks_generator for word in
             text_in_single_block.split()))

        # We get the words in div blocks
        text_in_div_blocks_generator = (''.join(div_tag.findAll(text=True)) for div_tag in self.soup.findAll('div'))
        counter_for_div_blocks = Counter(
            (word.rstrip(punctuation).lower() for text_in_single_block in text_in_div_blocks_generator for word in
             text_in_single_block.split()))

        total = counter_for_p_blocks + counter_for_div_blocks
        return sum(total.values())

    def find_word_on_page(self, word):
        return word.lower() in self.html_page.lower()


class Saver:
    @staticmethod
    def save_to_csv(languages, file_path):
        with open(file_path, 'w') as csv_file:
            writer = csv.writer(csv_file)
            writer.writerow(('Programming Language', 'Rating(%)'))
            writer.writerows((language.name, language.rating) for language in languages)


def main():
    scrap = Scrapper()
    languages = scrap.parse_top_programming_languages()
    for language in scrap.languages:
        print(language, "\n")
    Saver.save_to_csv(languages, 'languages.csv')

    print("Amount of words on the page: {}".format(scrap.count_words_on_page()))

    word_to_be_found = "python"
    print("Is there is word {} on the page? ==> {}".format(word_to_be_found, scrap.find_word_on_page(word_to_be_found)))


if __name__ == '__main__':
    main()
