import os
import fitz
import json
import random
import tqdm
from pathlib import Path

if __name__ == "__main__":
    root_dir = Path(os.path.dirname(os.path.abspath(__file__)))
    images_dir = os.path.join(root_dir, Path("images"))
    labels_dir = os.path.join(root_dir, Path("labels"))
    pdfs_dir = os.path.join(root_dir, Path("pdfs"))
    for pdf in os.listdir(pdfs_dir):
        data = fitz.open(pdfs_dir / Path(pdf))
        for page in data:
            blocks = page.get_text("dict")["blocks"]
            lables = []
            for block in blocks:
                if 'lines' not in block:
                    continue
                lables.append(block)
            image = page.get_pixmap()
            pdf = pdf.rstrip('.pdf')
            image.save(images_dir / Path(pdf + str(page.number) + ".png"))
            with open(labels_dir / Path(pdf + str(page.number) + ".json"), "w") as f:
               json.dump(lables, f, indent=4)