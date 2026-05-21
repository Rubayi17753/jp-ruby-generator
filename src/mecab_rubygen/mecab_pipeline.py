import MeCab
import config
import conzt
import src.utils as ut 

if config.DIC == 'unidic':
    import unidic_lite
    tagger = MeCab.Tagger(fr'-r nul -d "{unidic_lite.DICDIR}"')
elif config.DIC == 'ipadic':
    import ipadic
    tagger = MeCab.Tagger(fr'-r nul -d "{ipadic.DICDIR}"')

if config.TRANSLIT in ('nihon', 'kunrei'):
    from src.kanji_to_kunreisiki import kana_converter 
else:
    kana_converter = None

def _kana_pairs_core(text):

    pairs = []
    node = tagger.parseToNode(text)
    while node:

        surf = node.surface
        kana = ''
        feat = node.feature.split(',')

        if ut.has_kanji(surf) and config.RUBY_KANJI:
            kana = feat[config.MECAB_KANA_ROW] if len(feat) > config.MECAB_KANA_ROW else ''

        elif ut.has_katakana(surf) and config.RUBY_KATAKANA:
            kana = surf

        elif ut.has_hiragana(surf) and config.RUBY_HIRAGANA:
            kana = surf

        pairs.append((surf, kana))  

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
    
    def _reconstitute(pairs):
        def bracketify(rub):
            return f'({rub})' if rub else ''
        text = [f'{s}{bracketify(rub)}' for s, rub in pairs]
        return text

elif config.OUTPUT_LAYOUT == 'md':

    def _reconstitute(pairs):
        def segm(s, rub):
            if rub:
                return f'<ruby>{s}<rp>（</rp><rt>{rub}</rt><rp>）</rp></ruby>'
            else:
                return s
        text = [segm(s, rub) for s, rub in pairs]
        return text
 
def reconstitute_common(pairs):    
    text = _reconstitute(pairs)
    text = config.TOKEN_DELIM.join(text)
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
    
    text = reconstitute_common(pairs)
    text = text.replace(conzt.LINE_BREAK_SUB, '\n')
    text = text.replace(conzt.SPACE_SUB, ' ')

    return text


