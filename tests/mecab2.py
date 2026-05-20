import MeCab
import unidic_lite

tagger = MeCab.Tagger(
    fr'-r nul -d "{unidic_lite.DICDIR}"'
)

text = "私は、その男の写真を三葉、見たことがある。"

tagger.parse("")
tagger.parseNBestInit(text)

def main():
    for i in range(5):

        print(f"\n=== PARSE {i+1} ===")

        node = tagger.nextNode()

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