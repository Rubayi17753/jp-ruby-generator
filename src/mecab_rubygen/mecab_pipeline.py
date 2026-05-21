import MeCab
import unidic_lite
import config
import conzt
import src.utils as ut 

tagger = MeCab.Tagger(fr'-r nul -d "{unidic_lite.DICDIR}"')

if config.TRANSLIT in ('nihon', 'kunrei'):
    from src.kanji_to_kunreisiki import kana_converter 
else:
    kana_converter = None

def _kana_pairs_core(text):

    pairs = []
    node = tagger.parseToNode(text)
    while node:

        appended = 0
        surf = node.surface

        if config.RUBY_FOR == 'kanji_only':
            if not ut.has_kanji(surf):
                pairs.append((surf, ''))
                appended = 1

        if not appended:
            feat = node.feature.split(',')
            pairs.append((surf, feat[config.MECAB_KANA_ROW]))

        node = node.next

    return pairs

def kana_pairs(sentence):

    text2 = sentence.lstrip(conzt.RUBY_DELIM_L).rstrip(conzt.RUBY_DELIM_R)
    
    # kana pairs presupplied
    if len(sentence) != len(text2) and config.PREEXISTING_RUBY:
        if '|' in text2:
            pairs = [text2.split('|')]
        else:
            pairs = [(text2, '')]
    
    else:
        pairs = _kana_pairs_core(sentence)
    
    return pairs

if config.OUTPUT_LAYOUT == 'brackets':
    
    def reconstitute(pairs):
        def bracketify(rub):
            return f'({rub})' if rub else ''
        text = [f'{s}{bracketify(rub)}' for s, rub in pairs]
        text = ''.join(text)
        return text

elif config.OUTPUT_LAYOUT == 'md':

    def reconstitute(pairs):
        def segm(s, rub):
            if rub:
                return f'<ruby>{s}<rp>（</rp><rt>{rub}</rt><rp>）</rp></ruby>'
            else:
                return s
        text = [segm(s, rub) for s, rub in pairs]
        text = ''.join(text)
        return text

def rubify(text, ext):

    if ext in ('.html', '.htm'):
        text = ut.html_to_md(text)
    elif ext == '.md':
        pass
    elif ext == '.txt':
        pass
    
    text = text.replace('\n', conzt.LINE_BREAK_SUB)
    text = text.replace(' ', conzt.SPACE_SUB)
    sentences = ut.split_sentence(text)

    pairs = [pair for sentence in sentences for pair in kana_pairs(sentence)]
    if kana_converter:
        pairs = [(a, kana_converter(b)) for a, b in pairs]
    
    text = reconstitute(pairs)
    text = text.replace(conzt.LINE_BREAK_SUB, '\n')
    text = text.replace(conzt.SPACE_SUB, ' ')

    return text


