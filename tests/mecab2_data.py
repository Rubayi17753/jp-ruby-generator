import MeCab
import unidic_lite
import config
import src.utils as ut 

tagger = MeCab.Tagger(
    fr'-r nul -d "{unidic_lite.DICDIR}"'
)

def kana_pairs(text):

    pairs = []
    node = tagger.parseToNode(text)
    while node:

        surf = node.surface

        if config.RUBY_FOR_KANJI_ONLY:
            if surf and ut.has_kanji(surf):
                feat = node.feature.split(',')
                pairs.append((surf, feat[config.MECAB_KANA_ROW]))
            else:
                pairs.append((surf, ''))
        else:
            pairs.append((surf, feat[config.MECAB_KANA_ROW]))

        node = node.next

    return pairs

def main():
    text = "一葉は、その男の、幼年時代、とでも言うべきであろうか、十歳前後かと推定される頃の写真であって、その子供が大勢の女のひとに取りかこまれ、（それは、その子供の姉たち、妹たち、それから、従姉妹いとこたちかと想像される）庭園の池のほとりに、荒い縞の袴はかまをはいて立ち、首を三十度ほど左に傾け、醜く笑っている写真である。"
    print(kana_pairs(text))
    
if __name__ == "__main__":
    main()