import MeCab

tagger = MeCab.Tagger()
text = "私は、その男の写真を三葉、見たことがある。"
nbest = 5

def main():
    for i in range(nbest):
        result = tagger.next()

    # Required warm-up call in some MeCab builds
    tagger.parse("")

    # Initialize N-best parsing
    tagger.parseNBestInit(text)

    for i in range(nbest):
        print("=" * 40)
        print(f"PARSE {i+1}")
        print("=" * 40)

        parsed = tagger.next()

        if parsed is None:
            break

        print(parsed)