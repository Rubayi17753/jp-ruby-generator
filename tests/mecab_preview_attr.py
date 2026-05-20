import MeCab
import unidic_lite

tagger = MeCab.Tagger(
    fr'-r nul -d "{unidic_lite.DICDIR}"'
)

def preview_attr(text):

    feature_lists = list()
    node = tagger.parseToNode(text)
    while node:

        if node.surface:

            print("SURFACE:")
            print(node.surface)

            print("\nFEATURE STRING:")
            feat = node.feature
            print(feat)
            feature_lists.append(feat.split(','))

            print("\nNODE ATTRIBUTES:")

            for attr in dir(node):

                if not attr.startswith("_"):

                    try:
                        value = getattr(node, attr)

                        # Avoid noisy linked-node output
                        if attr not in ("next", "prev", "enext", "bnext"):

                            print(f"{attr}: {value}")

                    except Exception as e:
                        print(f"{attr}: <ERROR: {e}>")

        node = node.next

    feature_lists = list(map(list, zip(*feature_lists)))
    feature_lists = [f"{i}\t{' '.join(fl)}" for i, fl in enumerate(feature_lists)]
    feature_lists = '\n'.join(feature_lists)
    print(feature_lists)


def main():

    text = "想像 まんざら空からお世辞に聞えないくらいの"
    preview_attr(text)