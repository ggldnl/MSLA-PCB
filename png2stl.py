from pathlib import PurePath
from skimage import measure
from stl import mesh
import numpy as np
import pdf2image
import argparse
import cv2
import os


def get_local_folder():
    """
    Returns the PurePath of the project folder
    """

    try:
        return PurePath(os.path.dirname(os.path.realpath(__file__)))  # py
    except NameError:
        pass
    return os.path.abspath("")  # ipynb


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


def _unpad(x, pad_width):
    slices = []
    for c in pad_width:
        e = None if c[1] == 0 else -c[1]
        slices.append(slice(c[0], e))
    return x[tuple(slices)]


def preprocess (image, invert=False, hmirror=False, vmirror=True):
    """
    Prepares the image for the conversion

    Attributes
    ----------
    image: np.array
        Numpy array containing an rgb image
    
    invert: bool
        True if we have to invert the image; input images should be black (traces) 
        on white (non-conductive surface)

    hmirror: bool
        True if we have to horizontally mirror the image

    vmirror: bool
        True if we have to vertically mirror the image; this needs to be done
        in order to successfully print a circuit with a SLA printer

    Returns
    -------
    The preprocessed image ready to be converted to a 3d object

    Throws
    ------
    ValueError
        if the input is not a suitable numpy array
    """

    if len(image.shape) < 2 or len(image.shape) > 3:
        raise ValueError(f'Invalid shape [{image.shape}] for image array')

    # grayscale the image
    if len(image.shape) == 3:
        image = np.mean(image, axis=2, dtype=bool)

    # TODO
    # threshold the image so that we end up with only two colors, black and white

    # pdfs generated by cad softwares often come with a border

    # find top padding
    top_padding = -1
    previous_row_content = np.unique(image[0])
    for i in range(1, len(image)):
        current_row_content = np.unique(image[i])
        if not np.array_equal(current_row_content, previous_row_content):
            break
        previous_row_content = current_row_content
        top_padding += 1

    # find bottom padding
    bottom_padding = -1
    previous_row_content = np.unique(image[-1])
    for i in range(len(image) - 1, 0, -1):
        current_row_content = np.unique(image[i])
        if not np.array_equal(current_row_content, previous_row_content):
            break
        previous_row_content = current_row_content
        bottom_padding += 1

    # find left padding
    left_padding = -1
    previous_col_content = np.unique(image[:, 0])
    for i in range(1, len(image[0])):
        current_col_content = np.unique(image[:, i])
        if not np.array_equal(current_col_content, previous_col_content):
            break
        previous_col_content = current_col_content
        left_padding += 1

    # find right padding
    right_padding = -1
    previous_col_content = np.unique(image[:, -1])
    for i in range(len(image[0]) - 1, 1, -1):
        current_col_content = np.unique(image[:, i])
        if not np.array_equal(current_col_content, previous_col_content):
            break
        previous_col_content = current_col_content
        right_padding += 1

    pad = ((top_padding, bottom_padding),(left_padding, right_padding))

    # unpad
    image = _unpad(image, pad)

    if invert:
        image = ~image

    if hmirror:
        image = np.flip(image, 0)

    if vmirror:
        image = np.flip(image, 1)
    
    return image


def numpy_to_stl(mask, output_shape):
    """
    Converts the 3d mask into a 3d object using the marching cube
    algorithm. The 3d object will have the dimensions specified
    by the output_shape parameter (mm).

    Attributes
    ----------
    mask: np.array
        2d nunpy array to erode into a 3d stl object
    
    output_shape: int tuple
        size in mm of the output 3d object

    Returns
    -------
    The 3d stl object
    """

    width, depth, height = output_shape

    mask = np.repeat(mask[:, :, np.newaxis], 3, axis=2)

    # contour of the object
    mask = np.pad(mask, ((1, 1), (1, 1), (1, 1)), constant_values=True)

    #import matplotlib.pyplot as plt
    #plt.imshow(mask[:, :, 1])

    # create the 3d meshgrid
    shp = mask.shape
    x = np.linspace(0, width, shp[1])
    y = np.linspace(0, depth, shp[0])
    z = np.linspace(0, height, shp[2])

    # get vertices and faces
    verts, faces, normals, values = measure.marching_cubes(mask)

    # scaling
    dx = np.diff(x)[0]
    dy = np.diff(y)[0]
    dz = np.diff(z)[0]
    dr = np.array([dx, dy, dz])
    verts = verts * dr

    # build the 3d object
    obj_3d = mesh.Mesh(np.zeros(faces.shape[0], dtype=mesh.Mesh.dtype))
    for i, f in enumerate(faces):
        obj_3d.vectors[i] = verts[f]

    return obj_3d


if __name__ == '__main__':

    # ----------------------------- argument handling ---------------------------- #

    parser = argparse.ArgumentParser()

    parser.add_argument('filename') # e.g. ./samples/load_sharing_panelized.png
    parser.add_argument('size', nargs='+', type=int) # e.g. -s 18 25 1

    args = parser.parse_args()

    size = tuple(args.size)
    input_path = PurePath(args.filename)

    # ----------------------------------- main ----------------------------------- #

    stem = input_path.stem
    suffix = input_path.suffix.lower()
    folder = input_path.parent

    if suffix.endswith('.pdf'):
        # Some softwares (e.g. easyEDA) let you export the pcb as a pdf file;
        # sometimes this is preferable since we can convert it to an image
        # specifying the DPIs, thus increasing the quality before conversion.
        #
        # Read the pdf file, get an image from it and save it in the same
        # folder, with the same name (except of course the extension)
        img = pdf_2_np(input_path, dpi=400)
        
        image_path = PurePath(folder, stem + '.png')
        cv2.imwrite(str(image_path), img)

    elif suffix.endswith('.png'):
        
        img = cv2.imread(str(input_path))

    else:
        raise ValueError(f'Invalid input file: {input_path}')

    # we have the image as a numpy array, remove external padding
    # and apply other preprocessing steps
    img = preprocess(img, invert=False)

    # convert the image to 
    obj_3d = numpy_to_stl(img, size) # (width, depth, height)

    output_file = PurePath(folder, stem + '.stl')
    obj_3d.save(str(output_file))