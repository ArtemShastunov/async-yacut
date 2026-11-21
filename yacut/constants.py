import string

MAX_LENGTH_SHORT_ID = 16
AUTO_SHORT_ID_LENGTH = 6
MAX_SHORT_ID_ATTEMPTS = 100
ALLOWED_CHARS = string.ascii_letters + string.digits
SHORT_ID_REGEX = r"^[a-zA-Z0-9]+$"
RESERVED_SHORT_IDS = {"files"}

YANDEX_DISK_API_URL = "https://cloud-api.yandex.net/v1/disk/resources"
