from markdownify import markdownify as md

def main():

    input_fp = 'samples/sample2.html'
    with open(input_fp, 'r', encoding='utf-8') as f:
        text = f.read()

    replacements = [
        ('<ruby>', '⟦'), ('</ruby>', '⟧'),
        ('<rp>（</rp>', ''), ('<rp>）</rp>', ''),
        ('<rb>', ''), ('</rb>', ''), 
        ('<rt>', '|'), ('</rt>', ''), 
    ]
    for a, b in replacements:
        text = text.replace(a, b)
    text_md = md(text)

    print(text_md)