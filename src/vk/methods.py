import vk_api
from vk_api.utils import get_random_id
from vk_api.keyboard import VkKeyboard


class VkBotHandler:
    def __init__(self, api: vk_api.VkApi) -> None:
        self._api = api

    def send_message(self, user_id: int, text: str,
                     attachments: list[str] = None,
                     markup: VkKeyboard.get_keyboard = None) -> None:
        params = {'user_id': user_id,
                  'message': text,
                  'random_id': get_random_id(),
                  'attachment': ','.join(
                      attachments) if attachments else None,
                  'keyboard': markup if markup else None}

        self._api.method('messages.send', params)
