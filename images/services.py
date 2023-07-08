import requests
import tempfile

from django.core.files import File

from images.models import Image


def attach_image_from_url(url: str, image: Image):
    response = requests.get(url, stream=True)

    if response.status_code != requests.codes.ok:
        raise ValueError("response img request is not ok")

    # Get the filename from the url, used for saving later
    file_name = url.split('/')[-1]

    # Create a temporary file
    lf = tempfile.NamedTemporaryFile()

    # Read the streamed image in sections
    for block in response.iter_content(1024 * 8):
        # If no more file then stop
        if not block:
            break

        # Write image block to temporary file
        lf.write(block)

    image.image.save(file_name + ".jpg", File(lf), save=True)
    image.thumbnail.save(file_name + ".jpg", File(lf), save=True)
