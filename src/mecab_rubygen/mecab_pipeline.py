import MeCab
import unidic_lite
import config
import src.utils as ut 

tagger = MeCab.Tagger(fr'-r nul -d "{unidic_lite.DICDIR}"')

if config.TRANSLIT in ('nihon', 'kunrei'):
    from src.kanji_to_kunreisiki import kana_converter 
else:
    kana_converter = None

def kana_pairs(text):

    pairs = []
    node = tagger.parseToNode(text)
    while node:

        surf = node.surface

        if config.RUBY_FOR == 'kanji_only':
            if surf and ut.has_kanji(surf):
                feat = node.feature.split(',')
                pairs.append((surf, feat[config.MECAB_KANA_ROW]))
            else:
                pairs.append((surf, ''))
        elif config.RUBY_FOR == 'all':
            pairs.append((surf, feat[config.MECAB_KANA_ROW]))

        node = node.next

    return pairs

if config.OUTPUT_LAYOUT == 'brackets':
    
    def reconstitute(pairs):
        def bracketify(rub):
            return f'({rub})' if rub else ''
        text = [f'{s} {bracketify(rub)} ' for s, rub in pairs]
        text = ''.join(text)
        return text


def rubify(text):
    sentences = ut.split_sentence(text)

    pairs = [pair for sentence in sentences for pair in kana_pairs(sentence)]
    if kana_converter:
        pairs = [(a, kana_converter(b)) for a, b in pairs]
    
    text = reconstitute(pairs)

    print(text)
    exit()


