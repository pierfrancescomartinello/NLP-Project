from src.preprocessor import remove_nonbreaking

#TODO remove this file
def test_remove_nonbreaking():
    assert "\xa0" not in remove_nonbreaking("ciao\xa0")
    assert "\xa0" not in remove_nonbreaking("ciao\xa0\xa0")
