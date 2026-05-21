import sys
from .mecab_pipeline import rubify

def main():
    fp_input = sys.argv[1]
    with open(fp_input, 'r', encoding='utf-8') as f:
        text = f.read()
    
    rubify(text)

if __name__ == "__main__":
    main()