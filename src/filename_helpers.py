import os

SUPPORTED_IMAGE_SUFFIXES = ["jpg"]
SUPPORTED_VIDEO_SUFFIXES = ["mp4"]


def get_lower_case_file_suffix(path):
    file_suffix = path.split('.')[-1].lower()
    return file_suffix


def is_image(path):
    file_suffix = get_lower_case_file_suffix(path)
    return file_suffix in SUPPORTED_IMAGE_SUFFIXES


def is_video(path):
    file_suffix = get_lower_case_file_suffix(path)
    return file_suffix in SUPPORTED_VIDEO_SUFFIXES


def get_versioned_file_path(path):
    if not os.path.exists(path):
        return path

    filename, extension = os.path.splitext(path)
    version_conter = 2

    while os.path.exists(path):
        path = filename + "_v" + str(version_conter) + extension
        version_conter += 1

    return path
