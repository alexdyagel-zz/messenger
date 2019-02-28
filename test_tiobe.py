import pytest
import tiobe_parser
import os


class TestTiobeWebsite:
    @pytest.fixture
    def scrap_tiobe(self):
        scrap_tiobe = tiobe_parser.Scrapper()
        scrap_tiobe.parse_top_programming_languages()
        return scrap_tiobe

    @pytest.mark.parametrize("word_on_page", ["quality", "TIOBE", "software", "framework", "language", "programming"])
    def test_word_is_on_page(self, scrap_tiobe, word_on_page):
        assert scrap_tiobe.find_word_on_page("python") is True

    def test_java_is_better_than_c_sharp(self, scrap_tiobe):
        assert scrap_tiobe.get_rating_of_language("Java") > scrap_tiobe.get_rating_of_language("C#")

    @pytest.mark.parametrize("other_language", ["C#", "C++", "PHP", "Perl", "R", "Go", "Swift"])
    def test_python_is_better_than_some_other_languages(self, scrap_tiobe, other_language):
        assert scrap_tiobe.get_rating_of_language("Python") > scrap_tiobe.get_rating_of_language(other_language)

    def test_website_has_a_lot_of_words(self, scrap_tiobe):
        big_number = 1000
        assert scrap_tiobe.count_words_on_page() > big_number

    @pytest.mark.parametrize("bad_word", ["shit", "fuck", "crap"])
    def test_website_is_suitable_for_children(self, scrap_tiobe, bad_word):
        assert scrap_tiobe.find_word_on_page(bad_word) is False

    def test_creating_of_csv_file(self, scrap_tiobe):
        file_to_save = "languages.csv"
        tiobe_parser.Saver.save_to_csv(scrap_tiobe.languages, file_to_save)
        assert os.path.isfile(file_to_save) is True


class TestBlankWebsite:
    @pytest.fixture
    def scrap_blank(self):
        return tiobe_parser.Scrapper("http://blank.org/")

    def test_there_are_no_words_on_blank_website(self, scrap_blank):
        assert scrap_blank.count_words_on_page() == 0
