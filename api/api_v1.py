import io
import numpy
from PIL import Image
from backend.ugatit.wrapper import UgatitWrapper


class GanApi:
    """
    Class contains API methods for bot
    """

    def __init__(self) -> None:
        """
        Constructor
        """
        self.__handler_class: UgatitWrapper = UgatitWrapper()

    async def selfie2anime(self, selfie: io.BytesIO) -> io.BytesIO:
        """
        Transform selfie to anime image
        :param selfie: image as io.BytesIO
        :return: anime image as io.BytesIO
        """
        numpy_image: numpy.ndarray = self.__bytesio2numpy(selfie)
        processed_image: numpy.ndarray = self.__handler_class.selfie2anime(input_image=numpy_image)
        image_bytes: io.BytesIO = self.__numpy2bytesio(processed_image)
        return image_bytes

    async def anime2selfie(self, anime_image: io.BytesIO) -> io.BytesIO:
        """
        Transform anime to selfie
        :param anime_image: anime image as io.BytesIO
        :return: image as io.BytesIO
        """
        numpy_image: numpy.ndarray = self.__bytesio2numpy(anime_image)
        processed_image: numpy.ndarray = self.__handler_class.anime2selfie(input_image=numpy_image)
        image_bytes: io.BytesIO = self.__numpy2bytesio(processed_image)
        return image_bytes

    @staticmethod
    def __numpy2bytesio(numpy_image: numpy.ndarray) -> io.BytesIO:
        """
        Convert numpy image to io.BytesIO image
        :param numpy_image: image as numpy.ndarray
        :return: image as io.BytesIO
        """
        out_picture: io.BytesIO = io.BytesIO()
        out_picture.name = 'selfie.jpeg'
        pil_image: Image.Image = Image.fromarray(numpy_image.astype('uint8'), 'RGB')
        pil_image.save(out_picture, 'JPEG')
        out_picture.seek(0)
        return out_picture

    @staticmethod
    def __bytesio2numpy(inp_bytes: io.BytesIO) -> numpy.ndarray:
        """
        Convert io.BytesIO image to numpy image
        :param inp_bytes: image as io.BytesIO
        :return: image as numpy.ndarray
        """
        inp_bytes.seek(0)
        pil_image: Image.Image = Image.open(inp_bytes)
        numpy_image = numpy.asarray(pil_image)
        return numpy_image
