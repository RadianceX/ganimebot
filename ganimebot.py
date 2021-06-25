import io
import logging
from aiogram import Bot, Dispatcher, types, executor
from api.api_v1 import GanimeBotApi
from io import BytesIO
from PIL import Image
import numpy
import configparser


class GanimeBot:
    """
    TODO: add description
    """
    def __init__(self, api_token: str) -> None:
        """
        TODO: add description
        """
        self.__setup_logger()
        self._api = GanimeBotApi()
        self._bot = Bot(token=api_token)
        self._dp = Dispatcher(self._bot)
        self._setup_handlers()

    def __setup_logger(self) -> None:
        """
        TODO: add description
        :return:
        """
        stream_handler: logging.StreamHandler = logging.StreamHandler()
        stream_handler.setLevel(logging.INFO)
        stream_handler.setFormatter(logging.Formatter('%(asctime)s [%(levelname)s] - %(message)s'))

        self._logger: logging.Logger = logging.getLogger(__file__)
        self._logger.setLevel(logging.INFO)
        self._logger.addHandler(stream_handler)

    def start(self) -> None:
        """
        TODO: add description
        :return:
        """
        self._logger.info('Bot started')
        executor.start_polling(self._dp, skip_updates=True)

    async def send_welcome(self, message: types.Message) -> None:
        """
        TODO: add description
        Bot is under de `/start` or `/help` command
        """
        await message.reply("Bot is under development. Send photo only")

    async def handle_docs_photo(self, message: types.Message) -> None:
        """
        TODO: add description
        :param message:
        :return:
        """
        file_id: str = message.photo[-1].file_id
        file: types.File = await self._bot.get_file(file_id)
        file_path: str = file.file_path

        inp_file: io.BytesIO = await self._bot.download_file(file_path)
        anime2photo_file: io.BytesIO = await self._api.anime2photo(inp_file)
        photo2anime_file: io.BytesIO = await self._api.photo2anime(inp_file)

        media: types.MediaGroup = types.MediaGroup()
        media.attach_photo(types.InputFile(anime2photo_file))
        media.attach_photo(types.InputFile(photo2anime_file))

        await message.reply_media_group(media=media)

    def _setup_handlers(self) -> None:
        """
        TODO: add description
        :return:
        """
        self._dp.register_message_handler(self.send_welcome, commands=['help', 'start'])
        self._dp.register_message_handler(self.handle_docs_photo, content_types=['photo'])


if __name__ == '__main__':
    parser: configparser.ConfigParser = configparser.ConfigParser()
    parser.read("bot.conf")
    api_key: str = parser.get("config", "API_TOKEN")

    bot: GanimeBot = GanimeBot(api_key)
    bot.start()
