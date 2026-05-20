import MeCab
import unidic_lite

tagger = MeCab.Tagger(
    fr'-r nul -d "{unidic_lite.DICDIR}"'
)

text = "一葉は、その男の、幼年時代、とでも言うべきであろうか、十歳前後かと推定される頃の写真であって、その子供が大勢の女のひとに取りかこまれ、（それは、その子供の姉たち、妹たち、それから、従姉妹いとこたちかと想像される）庭園の池のほとりに、荒い縞の袴はかまをはいて立ち、首を三十度ほど左に傾け、醜く笑っている写真である。"

def main():

    node = tagger.parseToNode(text)

    surfaces = []
    kanas = []

    while node:

        if node.surface:

            surfaces.append(node.surface)
            feat = node.feature.split(",")

            # UniDic reading position
            kana = feat[9] if len(feat) > 9 else ""
            kanas.append(kana)

        node = node.next

    print("SURFACE:")
    print(" ".join(surfaces))

    print("KANA:")
    print(" ".join(kanas))


if __name__ == "__main__":
    main()