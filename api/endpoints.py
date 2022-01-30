__all__ = ['Mojang']


class BaseURL:
    """
    Класс описывающий конечную точку URL адреса.
    То есть корневой URL, к которому могут быть добавлены подкаталоги.
    """
    def __init__(self, url):
        """
        @param url: корневой URL
        """
        object.__setattr__(self, 'url', url)

    def __setattr__(self, key, value):
        if isinstance(value, str):
            object.__setattr__(self, key, self.__dict__['url'] + value)
        else: raise AttributeError('BaseURL class attributes must be only a str type!')


class Mojang:
    API             = BaseURL('https://api.mojang.com')
    AUTH            = BaseURL('https://authserver.mojang.com')
    SESSIONS        = BaseURL('https://session.minecraft.net')
    SESSION_SERVER  = BaseURL('https://sessionserver.mojang.com')

    API.SKIN                    = '/user/profile/{uuid}/skin'
    API.USERNAME_HISTORY        = '/user/profiles/{uuid}/names'
    API.USERNAME_TO_UUID        = '/users/profiles/minecraft/{username}'
    API.USERNAMES_TO_UUIDS      = '/profiles/minecraft'

    SESSION_SERVER.PLAYER_PROFILE = '/session/minecraft/profile/{uuid}'
