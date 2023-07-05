from vk_api.keyboard import VkKeyboard, VkKeyboardColor


class Markup:

    @staticmethod
    def start() -> VkKeyboard.get_keyboard:
        keyboard_start = VkKeyboard(one_time=True)
        keyboard_start.add_button('Начать',
                                  color=VkKeyboardColor.SECONDARY)
        return keyboard_start.get_keyboard()

    @staticmethod
    def sex() -> VkKeyboard.get_keyboard:
        keyboard_sex = VkKeyboard(one_time=True)
        keyboard_sex.add_button('М',
                                color=VkKeyboardColor.SECONDARY)
        keyboard_sex.add_button('Ж',
                                color=VkKeyboardColor.SECONDARY)
        return keyboard_sex.get_keyboard()

    @staticmethod
    def main() -> VkKeyboard.get_keyboard:
        keyboard_main = VkKeyboard(one_time=False)
        keyboard_main.add_button('Назад', color=VkKeyboardColor.NEGATIVE)
        keyboard_main.add_button('Далее', color=VkKeyboardColor.POSITIVE)
        keyboard_main.add_line()
        keyboard_main.add_button('Добавить в Избранное',
                                 color=VkKeyboardColor.PRIMARY)
        keyboard_main.add_openlink_button('Страница пользователя',
                                          link='https://github.com/netology-code/adpy-team-diplom/blob/main/README.md')
        return keyboard_main.get_keyboard()
