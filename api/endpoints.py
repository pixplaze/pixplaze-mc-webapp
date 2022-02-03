__all__ = ['Mojang']


class BaseURL:
    """
    Класс описывающий начальную точку URL адреса API.
    """
    def __init__(self, url):
        """
        @param url: корневой URL
        """
        object.__setattr__(self, 'url', url)

    def __setattr__(self, key, value):
        if isinstance(value, str):
            object.__setattr__(self, key, self.__dict__['url'] + value)
        else: raise TypeError('BaseURL class attributes must be only a str type!')


class Mojang:
    API             = BaseURL('https://api.mojang.com')
    AUTH            = BaseURL('https://authserver.mojang.com')
    SESSIONS        = BaseURL('https://session.minecraft.net')
    SESSION_SERVER  = BaseURL('https://sessionserver.mojang.com')

    API.SKIN                    = '/user/profile/{uuid}/skin'
    API.STATISTICS              = '/orders/statistics'
    API.UUID_TO_USERNAME        = '/user/profile/{uuid}'
    API.USERNAME_HISTORY        = '/user/profiles/{uuid}/names'
    API.USERNAMES_TO_UUIDS      = '/profiles/minecraft'
    API.USERNAME_TO_UUID        = '/users/profiles/minecraft/{username}'

    SESSION_SERVER.BLOCKED_SERVERS = '/blockedservers'
    SESSION_SERVER.PLAYER_PROFILE = '/session/minecraft/profile/{uuid}'


class Microsoft:
    AUTH = BaseURL(
        'https://login.live.com/oauth20_authorize.srf?client_id' +
        '=000000004C12AE6F&redirect_uri=https://login.live.com' +
        '/oauth20_desktop.srf&scope=service::user.auth.xboxlive.com::' +
        'MBI_SSL&display=touch&response_type=token&locale=en'
    )

    AUTH.REQUEST = ''
