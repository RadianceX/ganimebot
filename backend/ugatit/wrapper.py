import os.path
import cv2
import numpy
import tensorflow
from argparse import Namespace
from backend.ugatit.repo.UGATIT import UGATIT
import backend.ugatit.repo.main as ugatit_main
import backend.ugatit.repo.utils as ugatit_utils


class UgatitWrapper:
    """
    Wrapper for UGATIT class.
    Provides interface for numpy.ndarray selfie processing
    """

    def __init__(self) -> None:
        """
        Constructor
        """
        # Need to override some default argument values to make everything works
        args: Namespace = ugatit_main.parse_args()
        self.__overwrite_args(args)

        # Setup TensorFlow
        tensorflow.get_logger().setLevel('ERROR')
        tf_session: tensorflow.Session = tensorflow.Session(config=tensorflow.ConfigProto(allow_soft_placement=True))
        tensorflow.global_variables_initializer().run(session=tf_session)

        # Setup UGATIT
        self.base_gan: UGATIT = UGATIT(tf_session, args)
        self.base_gan.build_model()
        self.base_gan.saver = tensorflow.train.Saver()
        self.base_gan.load(self.base_gan.checkpoint_dir)

    def selfie2anime(self, input_image: numpy.ndarray) -> numpy.ndarray:
        """
        Transform selfie to anime image
        :param input_image: image as numpy.ndarray
        :return: anime image as numpy.ndarray
        """
        input_image: numpy.ndarray = numpy.asarray(self.__image_preprocessing(image=input_image))
        gan_image: numpy.ndarray = self.base_gan.sess.run(
            self.base_gan.test_fake_B,
            feed_dict={
                self.base_gan.test_domain_A: input_image
            }
        )
        output_image: numpy.ndarray = self.__image_postprocessing(gan_image)
        return output_image

    def anime2selfie(self, input_image: numpy.ndarray) -> numpy.ndarray:
        """
        Transform selfie to anime image
        :param input_image: anime image as numpy.ndarray
        :return: image as numpy.ndarray
        """
        input_image: numpy.ndarray = numpy.asarray(self.__image_preprocessing(image=input_image))
        gan_image: numpy.ndarray = self.base_gan.sess.run(
            self.base_gan.test_fake_A,
            feed_dict={
                self.base_gan.test_domain_B: input_image
            }
        )
        output_image: numpy.ndarray = self.__image_postprocessing(gan_image)
        return output_image

    def __image_preprocessing(self, image: numpy.ndarray) -> numpy.ndarray:
        """
        Some weird transformations taken from original UGATIT code
        :param image: image as numpy.ndarray
        :return: image as numpy.ndarray
        """
        size: int = self.base_gan.img_size
        image: numpy.ndarray = cv2.resize(image, dsize=(size, size))
        image = numpy.expand_dims(image, axis=0)
        image = image / 127.5 - 1
        return image

    def __image_postprocessing(self, image: numpy.ndarray) -> numpy.ndarray:
        """
        Some weird transformations taken from original UGATIT code
        :param image: image as numpy.ndarray
        :return: image as numpy.ndarray
        """
        size: list = [1, 1]
        image: numpy.ndarray = ((image + 1.) / 2) * 255.0
        image = ugatit_utils.merge(image, size)
        return image

    def __overwrite_args(self, args: Namespace) -> None:
        """
        Updated arguments in passed object to:
            --light True
            --phase test
            --checkpoint_dir ./backend/ugatit/repo/checkpoint
            --result_dir ./backend/ugatit/repo/results
            --log_dir ./backend/ugatit/repo/logs
            --sample_dir ./backend/ugatit/repo/samples
        :param args: argparse.Namespace object
        """
        args.light = True
        args.phase = 'test'
        args.checkpoint_dir = os.path.abspath('./backend/ugatit/checkpoints').replace('\\', '/')
        args.result_dir = os.path.abspath('./backend/ugatit/repo/results').replace('\\', '/')
        args.log_dir = os.path.abspath('./backend/ugatit/repo/logs').replace('\\', '/')
        args.sample_dir = os.path.abspath('./backend/ugatit/repo/samples').replace('\\', '/')
