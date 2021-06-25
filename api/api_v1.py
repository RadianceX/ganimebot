import io
from PIL import Image
from backend.ugatit.main import UgatitEnhanced
import numpy


class GanimeBotApi:
    """
    TODO: add description
    """
    def __init__(self) -> None:
        """
        TODO: add description
        """
        self.__handler_class: UgatitEnhanced = UgatitEnhanced()

    async def photo2anime(self, image: io.BytesIO) -> io.BytesIO:
        """
        TODO: add description
        :param image:
        :return:
        """
        numpy_image: numpy.ndarray = self.__bytesio2numpy(image)
        processed_image: numpy.ndarray = self.__handler_class.photo2anime(input_image=numpy_image)
        image_bytes: io.BytesIO = self.__numpy2bytesio(processed_image)
        return image_bytes

    async def anime2photo(self, image: io.BytesIO) -> io.BytesIO:
        """
        TODO: add description
        :param image:
        :return:
        """
        numpy_image: numpy.ndarray = self.__bytesio2numpy(image)
        processed_image: numpy.ndarray = self.__handler_class.anime2photo(input_image=numpy_image)
        image_bytes: io.BytesIO = self.__numpy2bytesio(processed_image)
        return image_bytes

    def __numpy2bytesio(self, out_pic: numpy.ndarray) -> io.BytesIO:
        """
        TODO: add description
        :param out_pic:
        :return:
        """
        out_bytesio: io.BytesIO = io.BytesIO()
        out_bytesio.name = 'image.jpeg'
        pil_image: Image.Image = Image.fromarray(out_pic.astype('uint8'), 'RGB')
        pil_image.save(out_bytesio, 'JPEG')
        out_bytesio.seek(0)
        return out_bytesio

    def __bytesio2numpy(self, bytes: io.BytesIO) -> numpy.ndarray:
        """
        TODO: add description
        :param bytes:
        :return:
        """
        bytes.seek(0)
        pil_image: Image.Image = Image.open(bytes)
        numpy_image = numpy.asarray(pil_image)
        return numpy_image
