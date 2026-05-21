import re
from markdownify import markdownify as md
import conzt

def has_kanji(text):
    return any(0x4E00 <= ord(c) <= 0x9FFF for c in text)

def has_hiragana(text):
    return any(0x3040 <= ord(c) <= 0x309F for c in text)

def has_katakana(text):
    return any(0x30A0 <= ord(c) <= 0x30FF for c in text)

def split_sentence(text):
    sentences = re.split(fr'(?<=[。！？{conzt.RUBY_DELIM_P}])', text)
    sentences = [s for s in sentences if s.strip()]
    sentences = [s.replace('⦁', '') for s in sentences]
    return sentences

def html_to_md(text):

    replacements = [
        ('<ruby>', f'{conzt.RUBY_DELIM_P}{conzt.RUBY_DELIM_L}'), 
        ('</ruby>', f'{conzt.RUBY_DELIM_R}{conzt.RUBY_DELIM_P}'),
        ('<rp>（</rp>', ''), ('<rp>）</rp>', ''),
        ('<rb>', ''), ('</rb>', ''), 
        ('<rt>', '|'), ('</rt>', ''), 
    ]
    for a, b in replacements:
        text = text.replace(a, b)
    text_md = md(text, strip='img')

    return text_md