import re

def has_kanji(text):
    return any(
        0x4E00 <= ord(c) <= 0x9FFF
        for c in text
    )

def split_sentence(text):
    sentences = re.split(r'(?<=[。！？])', text)
    sentences = [s for s in sentences if s.strip()]
    return sentences