import json
import codecs
from uuid import UUID
import requests as req
from requests import Session
from re import search, findall

from .endpoints import Mojang, Microsoft

# For test only

uuid = 'c01f3d0a58ca4aeaa1b95cf8f172b664'


# Utils

def warning(message='Функционал `{name}` пока не поддерживается!'):
    def outer(func):
        def inner(*args, **kwargs):
            raise DeprecationWarning(message.format(name=func.__name__))

        return inner

    return outer


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


# Mojang API wrappers

def username_to_uuid(username):
    """
    Функция-обёртка для Mojang API.
    Запрашивает `UUID` игрока или игроков по имени (или именам пользователей).
    @param username:
        имя пользователя типа `str`,
        или список имён пользователей типа `list`
    @return:
        `dict`, если передано одно имя в виде `str`,
        или `list`, если было передано несколько имён в виде `list`.
    """
    if isinstance(username, list):
        for name in username:
            if not validate_username(name):
                raise ValueError(f'Invalid username: {name}!')
        return req.post(Mojang.API.USERNAMES_TO_UUIDS, json=username).json()
    else:
        if not validate_username(username):
            raise ValueError(f'Invalid username: {username}!')
        return req.get(Mojang.API.USERNAME_TO_UUID.format(username=username)).json()


def uuid_to_username(uuid: str):
    """
    Функция-обёртка для Mojang API.
    Запрашивает имя пользователя по `uuid`.
    @param uuid: уникальный идентификатор пользователя;
    @return: `dict` c id пользователя и его именем.
    """
    if not validate_uuid(uuid):
        raise ValueError(f'Invalid UUID: {uuid}!')
    return req.get(Mojang.API.UUID_TO_USERNAME.format(uuid=uuid)).json()


def uuid_to_username_history(uuid: str):
    """
    Функция-обёртка для Mojang API.
    Запрашивает историю изменений имени профиля Minecraft.
    @param uuid: уникальный идентификатор пользователя;
    @return: `dict` cо списком истории его имён.
    """
    resp = req.get(Mojang.API.USERNAME_HISTORY.format(uuid=uuid)).json()
    return resp


def uuid_to_user_profile(uuid: str):
    """
    Функция-обёртка для Mojang API.
    Запрашивает профиль игрока по `uuid`. Автоматически декодирует
    `property` `textures['value']` в json.
    @param uuid: уникальный идентификатор пользователя;
    @return: `dict` со структурой профиля игрока с декодированным
    `property` `textures['value']`.
    """
    if not validate_uuid(uuid):
        raise ValueError(f'Invalid player UUID: {uuid}!')
    resp = req.get(Mojang.SESSION_SERVER.PLAYER_PROFILE.format(uuid=uuid)).json()
    if 'error' in resp:
        raise ValueError(f'Player not found: {uuid}!')
    else:  # TODO: Изменить извлечение `value` на проход по списку `properties`
        decoded = base64_to_json(resp['properties'][0]['value'])
        resp['properties'][0]['value'] = decoded
    return resp


def blocked_servers():
    """
    Функция-обёртка для Mojang API.
    Запрашивает заблокированные сервера.
    @return: текст SHA1 ip адресов, разделённые переносом строки.
    """
    return req.get(Mojang.SESSION_SERVER.BLOCKED_SERVERS).text


def statistics(json):
    """
    Функция-обёртка для Mojang API.
    Запрашивает статистику по ключам в списке, к примеру:
    {`metricKeys`: [
        'item_sold_minecraft', 'prepaid_card_redeemed_minecraft',
        'item_sold_cobalt', 'prepaid_card_redeemed_cobalt',
        'item_sold_dungeons', 'item_sold_scrolls'
    ]}
    @param json: `dict` с указынными ключами метрик.
    @return: `dict` со статистикой.
    """
    return req.post(Mojang.API.STATISTICS, json=json).json()


@warning()
def profile_information(): pass  # TODO


@warning()
def player_attributes(): pass  # TODO


@warning()
def profile_name_change_information(): pass  # TODO


@warning()
def check_product_voucher(): pass  # TODO


@warning()
def name_availability(username):
    return req.get(f'https://api.minecraftservices.com/minecraft/profile/name/{username}/available')


@warning()
def change_name(): pass  # TODO


@warning()
def change_skin(): pass  # TODO


@warning()
def upload_skin(): pass  # TODO


@warning()
def reset_skin(): pass  # TODO


@warning()
def hide_cape(): pass  # TODO


@warning()
def show_cape(): pass  # TODO


@warning()
def verify_security_location(): pass  # TODO


@warning()
def get_security_questions(): pass  # TODO


@warning()
def send_security_answers(): pass  # TODO


@warning()
def get_account_migration_information(): pass  # TODO


@warning()
def account_migration_otp(): pass  # TODO


@warning()
def verify_account_migration_otp(): pass  # TODO


@warning()
def submit_migration_token(): pass  # TODO


@warning()
def connect_xbox_live(): pass  # TODO


def base64_to_json(data):
    return json.loads(codecs.decode(data.encode(), 'base64').decode())


def get_microsoft_auth_url(sess: Session):
    resp = sess.get(Microsoft.AUTH.REQUEST)
    html_page = resp.text
    sFFTag = search(r'value="(.+?)"', html_page).group(1)
    urlPost = search(r"urlPost:'(.+?)'", html_page).group(1)
    return {'sFFTag': sFFTag, 'urlPost': urlPost}


def get_microsoft_token_url(sess: Session, login_data, auth):  # : Tuple[str, str] = field(default_factory=tuple)
    resp = sess.post(
        auth['urlPost'],
        params={
            'login': login_data[0],
            'loginfmt': login_data[0],
            'passwd': login_data[1],
            'PPFT': auth['sFFTag']})
    html_page = resp.text
    login_failed = True if search(r'Sign in to', html_page) else False
    two_factor = True if search(r'Help us protect your account', html_page) else False
    return resp, {'login_failed': login_failed}, {'two-factor authentication required': two_factor}


def parse_microsoft_token(url):
    import requests
    raw_login_data = url.split('#')[1]
    login_data = dict(item.split('=') for item in raw_login_data.split('&'))
    login_data['access_token'] = requests.utils.unquote(login_data["access_token"])  # URL decode the access token
    login_data["refresh_token"] = requests.utils.unquote(login_data["refresh_token"])  # URL decode the refresh token
    print(login_data)  # print the data
    return login_data


####################
def get_player_textures(uuid):
    profile = uuid_to_user_profile(uuid)
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


def bytes_to_image(image_bytes):
    from io import BytesIO
    return Image.open(BytesIO(image_bytes))


from PIL import Image


# image = Image.open('http://textures.minecraft.net/texture/d33ae38e6640b359d40d532f9436b741e3e0abf3f4e7731f7606749f5da38899')


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
