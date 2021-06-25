import configparser
import io
import logging
from aiogram import Bot, Dispatcher, types, executor
from api.api_v1 import GanApi


class GanimeBot:
    """
    GANime bot class
    """

    def __init__(self, api_token: str) -> None:
        """
        Constructor
        :param api_token: bot api token
        """
        self._logger = self.__setup_logger()
        self._api = GanApi()
        self._bot = Bot(token=api_token)
        self._dp = Dispatcher(self._bot)
        self.__setup_handlers()

    def start(self) -> None:
        """
        Starts the bot
        """
        self._logger.info('Bot started')
        executor.start_polling(self._dp, skip_updates=True)

    async def handle_help_message(self, message: types.Message) -> None:
        """
        Prints help message to the chat
        :param message: message object
        """
        self._logger.info(f"Handle help message from {message.chat.id}:{message.chat.username}")
        await message.reply('\n'.join([
            "Bot is under development.",
            "Send photo one by one.",
            "Type /help or /start to display this message.",
        ]))

    async def handle_photo_message(self, message: types.Message) -> None:
        """
        Download image sent by user and reply it with processed images
        :param message: message object
        """
        self._logger.info(f"Handle image message from {message.chat.id}:{message.chat.username}")
        # Retrieve image info
        image_file_id: str = message.photo[-1].file_id
        image_file: types.File = await self._bot.get_file(image_file_id)
        image_file_path: str = image_file.file_path

        # Download input image
        input_image_file: io.BytesIO = await self._bot.download_file(image_file_path)

        # Generate GAN images from input image
        anime2selfie_file: io.BytesIO = await self._api.anime2selfie(input_image_file)
        selfie2anime_file: io.BytesIO = await self._api.selfie2anime(input_image_file)

        # Add both images to group
        media: types.MediaGroup = types.MediaGroup()
        media.attach_photo(types.InputFile(anime2selfie_file))
        media.attach_photo(types.InputFile(selfie2anime_file))

        await message.reply_media_group(media=media)

    def __setup_handlers(self) -> None:
        """
        Setup handlers for commands and messages
        """
        self._dp.register_message_handler(self.handle_help_message, commands=['help', 'start'])
        self._dp.register_message_handler(self.handle_photo_message, content_types=['photo'])

    def __setup_logger(self) -> logging.Logger:
        """
        Configure logger
        :return: logger instance
        """
        stream_handler: logging.StreamHandler = logging.StreamHandler()
        stream_handler.setLevel(logging.INFO)
        stream_handler.setFormatter(logging.Formatter('%(asctime)s [%(levelname)s] - %(message)s'))

        logger: logging.Logger = logging.getLogger(__file__)
        logger.setLevel(logging.INFO)
        logger.addHandler(stream_handler)

        return logger


if __name__ == '__main__':
    # Load API key from config
    parser: configparser.ConfigParser = configparser.ConfigParser()
    parser.read("bot.conf")
    api_key: str = parser.get("config", "API_TOKEN")

    # Setup bot
    bot: GanimeBot = GanimeBot(api_key)
    bot.start()
