import pytest
from app.services.parsers.extractor import TextExtractor

def test_extract_text_from_txt():
    content = b"Hello World"
    text = TextExtractor.extract("test.txt", content)
    assert text == "Hello World"

def test_extract_unsupported_format():
    with pytest.raises(ValueError):
        TextExtractor.extract("test.xyz", b"content")
