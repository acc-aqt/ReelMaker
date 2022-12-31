SUPPORTED_IMAGE_SUFFIXES = ["jpg"]
SUPPORTED_VIDEO_SUFFIXES = ["mp4"]


def get_lower_case_file_suffix(file_name):
    file_suffix = file_name.split('.')[-1].lower()
    return file_suffix


def is_image(file_name):
    file_suffix = get_lower_case_file_suffix(file_name)
    return file_suffix in SUPPORTED_IMAGE_SUFFIXES


def is_video(file_name):
    file_suffix = get_lower_case_file_suffix(file_name)
    return file_suffix in SUPPORTED_VIDEO_SUFFIXES
