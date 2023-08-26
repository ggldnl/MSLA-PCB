from pathlib import PurePath
import numpy as np
import pdf2image
import argparse
import cv2


def pdf_2_np(filepath, dpi=400):  # 400 is a good trade-off
    """
    Given a single page pdf, convert it to image and return it as a numpy array.

    Attributes
    ----------
    filepath : str
        input pdf path

    dpi: int
        Dots Per Inch. By default, pdf2Image uses resolution of 92 DPI, 
        which is the typical screen resolution. Smaller DPI numbers result in 
        smaller images (e.g. suitable for use as thumbnails), while larger DPI 
        numbers generate larger images (e.g. suitable for high-quality output)
    
    Returns
    -------
    img: np.array
        Numpy array containing the single pdf page converted as image

    Throws
    ------
    ValueError
        if the pdf contains a number of pages different than the expected 1
    
    IOError
        for IO problems with the file
    """

    # the pdf contains only one page
    images = pdf2image.convert_from_path(filepath, dpi=dpi)

    if images is None:  # test if image exists and is read successfully
        raise IOError(f'Cannot find file: {str(filepath)}')
    
    if len(images) != 1:
        raise ValueError(f'Expected a single page pdf, got {len(images)} pages instead.')    

    # get the image data as array
    return np.asarray(images[0])


if __name__ == '__main__':

    # ----------------------------- argument handling ---------------------------- #

    parser = argparse.ArgumentParser()

    parser.add_argument('filename') # e.g. ./samples/load_sharing_panelized.png
    parser.add_argument('-o', '--output') # e.g. ./samples/output.png

    args = parser.parse_args()

    input_path = PurePath(args.filename)

    # TODO check
    output_path = PurePath(args.output)
    if output_path is None:
        output_path = PurePath(input_path.parent, input_path.stem + '.png')

    # ----------------------------------- main ----------------------------------- #

    # Some softwares (e.g. easyEDA) let you export the pcb as a pdf file;
    # sometimes this is preferable since we can convert it to an image
    # specifying the DPIs, thus increasing the quality before conversion.
    #
    # Read the pdf file, get an image from it and save it in the same
    # folder, with the same name (except of course the extension)

    img = pdf_2_np(input_path, dpi=400)
    cv2.imwrite(str(output_path), img)

