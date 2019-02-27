import pytest
import tiobe_parser
import os


class TestTiobeWebsite(object):
    def test_word_python_is_on_page(self):
        scrap = tiobe_parser.Scrapper()
        assert scrap.find_word_on_page("python") is True

    def test_there_are_no_words_on_blank_website(self):
        scrap = tiobe_parser.Scrapper("http://blank.org/")
        assert scrap.count_words_on_page() == 0

    def test_python_is_better_than_c_sharp(self):
        scrap = tiobe_parser.Scrapper()
        scrap.parse_top_programming_languages()
        assert scrap.get_rating_of_language("Python") > scrap.get_rating_of_language("C#")

    def test_java_is_better_than_c_sharp(self):
        scrap = tiobe_parser.Scrapper()
        scrap.parse_top_programming_languages()
        assert scrap.get_rating_of_language("Java") > scrap.get_rating_of_language("C#")

    def test_python_is_better_than_ruby(self):
        scrap = tiobe_parser.Scrapper()
        scrap.parse_top_programming_languages()
        assert scrap.get_rating_of_language("Python") > scrap.get_rating_of_language("Ruby")

    def test_website_has_a_lot_of_words(self):
        scrap = tiobe_parser.Scrapper()
        big_number = 1000
        assert scrap.count_words_on_page() > big_number

    def test_website_is_suitable_for_children(self):
        scrap = tiobe_parser.Scrapper()
        assert (scrap.find_word_on_page("fuck") and scrap.find_word_on_page("shit")) is False

    def test_creating_of_csv_file(self):
        scrap = tiobe_parser.Scrapper()
        languages = scrap.parse_top_programming_languages()
        file_to_save = "languages.csv"
        tiobe_parser.Saver.save_to_csv(languages, file_to_save)
        assert os.path.isfile(file_to_save) is True
