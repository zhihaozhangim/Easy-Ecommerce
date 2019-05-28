import os
import re
from typing import Union
from werkzeug.datastructures import FileStorage

from flask_uploads import UploadSet, IMAGES

# IMAGES: png, jpg...
IMAGE_SET = UploadSet("images", IMAGES)  # set name and allowed extensions, static/images/name


# Take FileStorage and save it to a folder
def save_image(image: FileStorage, folder: str = None, name: str = None) -> str:
    return IMAGE_SET.save(image, folder, name)  # static/images/name


# Take image and folder and return full path
def get_path(filename: str = None, folder: str = None) -> str:
    return IMAGE_SET.path(filename, folder)


# Take a filename and returns an image on any of the accepted format
def find_image_any_format(filename: str, folder: str) -> Union[str, None]:
    """
    Given a format-less filename, try to find the file by appending each of the allowed formats to the given
    filename and check if the file exists
    :param filename: formatless filename
    :param folder: the relative folder in which to search
    :return: the path of the image if exists, otherwise None
    """
    for _format in IMAGES:  # look for allowed extensions
        avatar = f"{filename}.{_format}"
        avatar_path = IMAGE_SET.path(filename=avatar, folder=folder)  # get the full path of the image
        if os.path.isfile(avatar_path):  # check whether it exists
            return avatar_path
    return None


# Take an FileStorage and return the file name
def _retrieve_filename(file: Union[str, FileStorage]) -> str:
    """
    Make our filename related functions generic, able to deal with FileStorage object as well as filename str.
    """
    if isinstance(file, FileStorage):
        return file.filename
    return file


# Check regex and return whether the string matches or not
def is_filename_safe(file: Union[str, FileStorage]) -> bool:
    """
    Check if a filename is secure according to our definition
    - starts with a-z A-Z 0-9 at least one time
    - only contains a-z A-Z 0-9 and _().-
    - followed by a dot (.) and a allowed_format at the end
    """
    filename = _retrieve_filename(file)

    allowed_format = "|".join(IMAGES)
    # format IMAGES into regex, eg: ('jpeg','png') --> 'jpeg|png'
    regex = f"^[a-zA-Z0-9][a-zA-Z0-9_()-\.]*\.({allowed_format})$"
    return re.match(regex, filename) is not None


# return full name of image in the path
def get_basename(file: Union[str, FileStorage]) -> str:
    """
    Return file's basename, for example
    get_basename('some/folder/image.jpg') returns 'image.jpg'
    """
    filename = _retrieve_filename(file)
    return os.path.split(filename)[1]   # os.path.split just split by the last /


# return file extension
def get_extension(file: Union[str, FileStorage]) -> str:
    """
    Return file's extension, for example
    get_extension('image.jpg') returns '.jpg'
    """
    filename = _retrieve_filename(file)
    return os.path.splitext(filename)[1]  # os.path.splitext split just by the last .
