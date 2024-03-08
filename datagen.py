import os
import fitz
import json
import random
from tqdm import tqdm
from pathlib import Path

fonts = json.load(open("fonts.json", "r"))
random.seed(10)

def process_labels(labels):
    res = []
    for block in labels:
        nblock = {}
        nblock["bbox"] = block["bbox"]
        if "lines" in block:
            nblock["lines"] = []
            for line in block['lines']:
                nline = {}
                nline["bbox"] = line["bbox"]
                nline["spans"] = []
                for span in line["spans"]:
                    nspan = {}
                    nspan["bbox"] = span["bbox"]
                    nspan["text"] = span["text"]
                    nspan["size"] = span["size"]
                    nspan.update(fonts[span["font"]])
                    nline["spans"].append(nspan)
                nblock["lines"].append(nline)
            nblock["image"] = False
        else:
            nblock["image"] = True
        res.append(nblock)
    return res

def modify_page(data, page):
    new_data = fitz.open()
    labels = []
    new_page = new_data.new_page(width=page.rect.width, height=page.rect.height)
    for block in page.get_text("dict")["blocks"]:
        if "lines" in block:
            # insert the lines into the new page with new font
            for line in block["lines"]:
                for span in line["spans"]:
                    new_font = random.choice(list(fonts.keys()))
                    new_page.insert_text(
                        (span["bbox"][0], span["bbox"][3]),
                        span["text"],
                        fontsize=span["size"],
                        fontname=new_font,
                    )
                    span["font"] = new_font
        else:
            # insert the image into the new page
            new_page.insert_image(
                block["bbox"],
                overlay=False,
                height=block["height"],
                width=block["width"],
                stream=block["image"],
            )
            pass
        labels.append(block)
    labels = process_labels(labels)
    return new_page, labels


def main():
    root_dir = Path(os.path.dirname(os.path.abspath(__file__)))
    images_dir = os.path.join(root_dir, Path("images"))
    labels_dir = os.path.join(root_dir, Path("labels"))
    pdfs_dir = os.path.join(root_dir, Path("pdfs"))
    for pdf in tqdm(os.listdir(pdfs_dir)):
        data = fitz.open(pdfs_dir / Path(pdf))
        for num in tqdm(range(100), leave=False):
            for page in data:
                modified_page, lables = modify_page(data, page)
                image = modified_page.get_pixmap()
                pdf = pdf.rstrip(".pdf")
                image.save(images_dir / Path(pdf + f"{num}_{page.number}" + ".png"))
                with open(labels_dir / Path(pdf + f"{num}_{page.number}" + ".json"), "w") as f:
                    json.dump(lables, f, indent=4)
        data.close()


if __name__ == "__main__":
    main()
    pass
