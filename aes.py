import urllib.parse
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad

KEY = "!&이걸보는;%"
IV = "사람은_안돼"


def encrypt(plain_file_id: str) -> str:
    cipher = AES.new(
        key=KEY.encode(),
        mode=AES.MODE_CBC,
        iv=IV.encode(),
    )
    return urllib.parse.quote(
        cipher.encrypt(pad(plain_file_id.encode(), 16)),
    )


def decrypt(encrypted_file_id: str) -> str:
    cipher = AES.new(
        key=KEY.encode(),
        mode=AES.MODE_CBC,
        iv=IV.encode(),
    )

    return unpad(
        cipher.decrypt(urllib.parse.unquote_to_bytes(encrypted_file_id)),
        16,
    ).decode()
