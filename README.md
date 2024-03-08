# Document Text Font Retrieval (DFTR) - Data
## Motivation
- There was a need for a dataset that focuses on the font used in the text present in the document (as expected by our solution)
- All existing datasets related to documents focused on document layout and context. There is no dataset that focuses on the font used in the document
- The dataset will be used to train a model that can predict the font used in the text present in the document along with their layout

## Existing Data Sets
### AdobeVFR
- Dataset covers 2,383 classes of popular fonts in graphics design
- Sufficiently large set of synthetic training data, tightly cropped, gray-scale, and size-normalized text images
- This is the closest thing we got to a dataset that focuses on the font used in the document

    * Problem: It does not contain the entire document image, instead, the image of the text is cropped and provided
    
