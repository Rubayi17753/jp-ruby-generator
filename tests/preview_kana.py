from fugashi import Tagger

tagger = Tagger()

def display_kana(text):
    for token in tagger(text):
        print(f"{token.surface} {token.feature.kana}")

def main():
    text = "今日。 今日は。今日は！"
    text = "彼は生きた魚を生け簀に入れた。"
    text = "今日は今日はと挨拶した。"
    display_kana(text)