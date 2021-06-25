import os.path
from argparse import Namespace
from backend.ugatit.repo.UGATIT import UGATIT
import backend.ugatit.repo.main as ugatit_main
import backend.ugatit.repo.utils as ugatit_utils
import numpy
import cv2
import tensorflow


class UgatitEnhanced:
    """
    TODO: add description
    """
    def __init__(self):
        """
        TODO: add description
        """
        args: Namespace = ugatit_main.parse_args()
        self.__overwrite_args(args)

        tf_session: tensorflow.Session = tensorflow.Session(config=tensorflow.ConfigProto(allow_soft_placement=True))
        tensorflow.global_variables_initializer().run(session=tf_session)
        tensorflow.get_logger().setLevel('ERROR')

        self.base_gan: UGATIT = UGATIT(tf_session, args)
        self.base_gan.build_model()
        self.base_gan.saver = tensorflow.train.Saver()
        self.base_gan.load(self.base_gan.checkpoint_dir)

    def photo2anime(self, input_image: numpy.ndarray) -> numpy.ndarray:
        """
        TODO: add description
        :param input_image:
        :return:
        """
        input_image: numpy.ndarray = numpy.asarray(self.__image_preprocessing(img=input_image))

        gan_image: numpy.ndarray = self.base_gan.sess.run(
            self.base_gan.test_fake_B,
            feed_dict={
                self.base_gan.test_domain_A: input_image
            }
        )
        output_image: numpy.ndarray = self.__image_postprocessing(gan_image)
        return output_image

    def anime2photo(self, input_image: numpy.ndarray) -> numpy.ndarray:
        """
        TODO: add description
        :param input_image:
        :return:
        """
        input_image: numpy.ndarray = numpy.asarray(self.__image_preprocessing(img=input_image))

        gan_image: numpy.ndarray = self.base_gan.sess.run(
            self.base_gan.test_fake_A,
            feed_dict={
                self.base_gan.test_domain_B: input_image
            }
        )
        output_image: numpy.ndarray = self.__image_postprocessing(gan_image)
        return output_image

    def __image_preprocessing(self, img: numpy.ndarray) -> numpy.ndarray:
        """
        TODO: add description
        :param img:
        :return:
        """
        size: int = self.base_gan.img_size
        img: numpy.ndarray = cv2.resize(img, dsize=(size, size))
        img = numpy.expand_dims(img, axis=0)
        img = img / 127.5 - 1
        return img

    def __image_postprocessing(self, image: numpy.ndarray) -> numpy.ndarray:
        """
        TODO: add description
        :param image:
        :return:
        """
        size: list = [1, 1]
        image: numpy.ndarray = ((image + 1.) / 2) * 255.0
        image = ugatit_utils.merge(image, size)
        return image

    def __overwrite_args(self, args: Namespace) -> None:
        """
        TODO: add description
        :param args:
        :return:
        """
        args.light = True
        args.phase = 'test'
        args.checkpoint_dir = os.path.abspath('./backend/ugatit/repo/checkpoint').replace('\\', '/')
