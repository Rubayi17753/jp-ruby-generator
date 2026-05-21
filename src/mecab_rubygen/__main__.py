import sys
from pathlib import Path

import config
from .mecab_pipeline import rubify

def main():
    fp_input = sys.argv[1]
    p = Path(fp_input)
    without_ext = p.with_suffix('')
    ext_in = p.suffix

    with open(fp_input, 'r', encoding=config.ENCODING_IN) as f:
        text = f.read()

    text_rubified = rubify(text, ext_in)

    ext_out_dict = {'brackets' : '.txt', 'md' : '.md'}
    ext_out = ext_out_dict.get(config.OUTPUT_LAYOUT, '')
    fp_output = f'{without_ext}_rubified{ext_out}'
    with open(fp_output, 'w', encoding='utf-8') as f:
        f.write(text_rubified) 

if __name__ == "__main__":
    main()