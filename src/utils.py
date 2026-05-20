def has_kanji(text):
    return any(
        0x4E00 <= ord(c) <= 0x9FFF
        for c in text
    )