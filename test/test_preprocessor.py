from src.preprocessor import remove_linebreak


def test_remove_linebreak():
    assert "\xa0" not in remove_linebreak("ciao\xa0")
    assert "\xa0" not in remove_linebreak("ciao\xa0\xa0")
