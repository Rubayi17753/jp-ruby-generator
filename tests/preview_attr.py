from fugashi import Tagger

tagger = Tagger()

def display_attr(text):
    for token in tagger(text):
        print("=" * 40)
        print("SURFACE:", token.surface)
        print()

        print("TOKEN ATTRIBUTES")
        for attr in dir(token):
            if not attr.startswith("_"):
                try:
                    value = getattr(token, attr)
                    print(f"{attr}: {value}")
                except Exception as e:
                    print(f"{attr}: <ERROR: {e}>")

        print()
        print("FEATURE ATTRIBUTES")

        if hasattr(token, "feature"):
            for attr in dir(token.feature):
                if not attr.startswith("_"):
                    try:
                        value = getattr(token.feature, attr)
                        print(f"{attr}: {value}")
                    except Exception as e:
                        print(f"{attr}: <ERROR: {e}>")

def main():
    text = "私は、その男の写真を三葉、見たことがある。"
    text = "今日は今日はと挨拶した。"
    display_attr(text)