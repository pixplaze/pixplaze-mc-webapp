class Base:
    def __init__(self, url):
        self.url = url

    def __setattr__(self, key, value):
        if key != 'url':
            self.__dict__[key] = self.__dict__['url'] + value
        else: object.__setattr__(self, key, value)


class Mojang:
    API             = Base('https://api.mojang.com')
    AUTH            = Base('https://authserver.mojang.com')
    SESSIONS        = Base('https://session.minecraft.net')
    SESSION_SERVER  = Base('https://sessionserver.mojang.com')
    API.SKIN                    = '/user/profile/{uuid}/skin'
    API.USERNAME_HISTORY        = '/user/profiles/{uuid}/names'
    API.USERNAME_TO_UUID        = '/users/profiles/minecraft/{username}'
