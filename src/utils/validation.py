def is_valid_age(message: str) -> bool:
    if not message.isdigit() or int(message) < 18 or int(message) > 100:
        return False
    return True


def get_city(message: str, usr_api) -> str | None:
    params = {'q': message, 'count': 1}
    response = usr_api.method('database.getCities',
                              values=params).get('items')
    return response[0]['title'] if response else None
