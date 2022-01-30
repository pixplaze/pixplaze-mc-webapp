from uuid import UUID
import json
import requests as req
import codecs
from .endpoints import Mojang


def validate_uuid(uuid: str) -> bool:
    """
    Проверяет корректность `uuid`, (не пустая строка и не `None`,
    может ли быть преобразовано в `UUID` :see uuid.UUID.
    @param uuid: строка уникального идентификатора пользователя.
    @return bool: логическое значение, пройдена ли проверка.
    """
    try:
        UUID(uuid)
        return True
    except ValueError or TypeError:
        return False


def validate_username(username: str) -> bool:
    """
    Проверяет корректность `username` (не пустая строка и не `None`,
    длинна username между 3 и 16 символами включительно).
    @param username: проверяемое имя пользователя;
    @return bool: логическое значение, пройдена ли проверка.
    """
    if username and 3 <= len(username) <= 17: return True


def get_player_uuid(username):
    """
    Функция-обёртка над Mojang API для
    запроса `UUID` игрока или игроков по имени (или именам пользователей).
    @param username:
        имя пользователя типа `str`,
        или список имён пользователей типа `list`
    @return:
        `dict`, если передано одно имя в виде `str`,
        или `list`, если было передано несколько имён в виде `list`.
    """
    if isinstance(username, list):
        return req.post(Mojang.API.USERNAMES_TO_UUIDS, json=username).json()
    else:
        return req.get(Mojang.API.USERNAME_TO_UUID.format(username=username)).json()


def get_username_history(uuid):
    resp = req.get(Mojang.API.USERNAME_HISTORY.format(uuid=uuid)).json()
    return resp


def get_player_profile(uuid):
    resp = req.get(Mojang.SESSION_SERVER.PLAYER_PROFILE.format(uuid=uuid)).json()
    if 'error' in resp:
        raise AttributeError('Invalid player UUID!')
    else:
        decoded = base64_to_json(resp['properties'][0]['value'])
        resp['properties'][0]['value'] = decoded
    return resp


def blocked_servers(): pass  # TODO


def statistics(): pass  # TODO


def profile_information(): pass  # TODO


def player_attributes(): pass  # TODO


def profile_name_change_information(): pass  # TODO


def check_product_voucher(): pass  # TODO


def name_availability(username):
    return req.get(f'https://api.minecraftservices.com/minecraft/profile/name/{username}/available')


def change_name(): pass  # TODO


def change_skin(): pass  # TODO


def upload_skin(): pass  # TODO


def reset_skin(): pass  # TODO


def hide_cape(): pass  # TODO


def show_cape(): pass  # TODO


def verify_security_location(): pass  # TODO


def get_security_questions(): pass  # TODO


def send_security_answers(): pass  # TODO


def get_account_migration_information(): pass  # TODO


def account_migration_otp(): pass  # TODO


def verify_account_migration_otp(): pass  # TODO


def submit_migration_token(): pass  # TODO


def connect_xbox_live(): pass  # TODO


def base64_to_json(data):
    return json.loads(codecs.decode(data.encode(), 'base64').decode())


####################
def get_player_textures(uuid):
    profile = get_player_profile(uuid)
    textures = None
    for prop in profile['properties']:
        if prop['name'] == 'textures': textures = prop['value']
    for key, val in textures.items():
        if key == 'textures': return val
    return None


def get_player_skin_url(uuid):
    return get_player_textures(uuid)['SKIN']['url']


def get_player_skin_image(url):
    return req.get(url).content


def __bytes_to_image__(image_bytes):
    from io import BytesIO
    return Image.open(BytesIO(image_bytes))


from PIL import Image
#image = Image.open('http://textures.minecraft.net/texture/d33ae38e6640b359d40d532f9436b741e3e0abf3f4e7731f7606749f5da38899')


# uuid = 'c01f3d0a58ca4aeaa1b95cf8f172b664'
# resp = req.get(get_player_skin_url('c01f3d0a58ca4aeaa1b95cf8f172b664'))
# skin_bytes = resp.content
# file = open('skin0.png', 'wb')
# file.write(skin_bytes)
# file.close()


def get_player_face(img, result_size):
    return img.resize(size=result_size, box=(8, 8, 16, 16), resample=Image.BOX)


class Skin:
    __url__     = None
    __head__    = None

    @property
    def head(self):
        if self.__head__: return self.head
        else: pass  # TODO:
