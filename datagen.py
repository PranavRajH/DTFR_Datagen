import os
import fitz
import json
import random
import tqdm
from pathlib import Path

fonts = fitz.Base14_fontdict
del fonts['symb']
del fonts['zadb']

def modify_page(data, page):
    new_data = fitz.open()
    new_page = new_data.new_page(width=page.rect.width, height=page.rect.height)
    for block in page.get_text("dict")["blocks"]:
        if 'lines' in block:
            # insert the lines into the new page with new font
            for line in block["lines"]:
                for span in line["spans"]:
                    new_font = random.choice(list(fonts.keys()))
                    new_page.insert_text((span["bbox"][0], span["bbox"][3]), span['text'], fontsize=span["size"], fontname=new_font)
            
        else:
            pass
    return new_page
    # for block in page.get_text("dict")["blocks"]:
    #     if 'lines' not in block:
    #         continue
    #     for line in block["lines"]:
    #         for span in line["spans"]:
    #             page.insert_text((span["bbox"][0], span["bbox"][3]), " ", fontsize=span["size"])
    #             print("Span: ", span["text"], "Font: ", span["font"])
    #             new_font = random.choice(list(fonts.keys()))
    #             page.insert_text((span["bbox"][0], span["bbox"][3]), span['text'], fontsize=span["size"], fontname=new_font)
    #             print("New Font: ", new_font)
    # return page


def main():
    root_dir = Path(os.path.dirname(os.path.abspath(__file__)))
    images_dir = os.path.join(root_dir, Path("images"))
    labels_dir = os.path.join(root_dir, Path("labels"))
    pdfs_dir = os.path.join(root_dir, Path("pdfs"))
    for pdf in os.listdir(pdfs_dir):
        data = fitz.open(pdfs_dir / Path(pdf))
        for page in data:
            modified_page = modify_page(data, page)
            blocks = modified_page.get_text("dict")["blocks"]
            lables = []
            for block in blocks:
                if 'lines' not in block:
                    continue
                lables.append(block)
            image = modified_page.get_pixmap()
            pdf = pdf.rstrip('.pdf')
            image.save(images_dir / Path(pdf + str(page.number) + ".png"))
            with open(labels_dir / Path(pdf + str(page.number) + ".json"), "w") as f:
               json.dump(lables, f, indent=4)
        data.close()

if __name__ == "__main__":
    # main()
    pass