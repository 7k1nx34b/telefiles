from flask import *
from werkzeug.utils import secure_filename
from uuid import uuid4
from pyrogram import Client
import os
import aes
import io
import threading
import logging
import sys
import base64

logging.basicConfig(
    stream=sys.stdout,
    level=logging.INFO,
    format='(%(name)s) %(funcName)20s() %(asctime)s - %(levelname)s - %(message)s',
)

app = Flask(__name__, static_url_path='', template_folder='./templates')

client = Client(
    name='me',
    api_id=611335,
    api_hash='d524b414d21f4d37f08684c1df41ac9c',
    # https://raw.githubusercontent.com/archlinux/svntogit-community/packages/telegram-desktop/trunk/PKGBUILD
    workers=100,
    max_concurrent_transmissions=50,
)


@app.route('/', methods=['GET'])
async def root():
    return render_template('root.jinja')


@app.route('/upload', methods=['POST'])
async def upload():
    if 'file' not in request.files or request.files['file'].filename == '':
        return redirect('/')

    file = request.files['file']

    file_name = secure_filename(file.filename)
    path = f'./upload/{uuid4()}_{file_name}'

    file.save(path)
    try:
        res = await client.send_document(
            chat_id='me',
            document=open(path, 'rb'),
            file_name=file_name,
        )
    finally:
        os.remove(path)

    return {
        'encrypted': aes.encrypt(
            res.document.file_id
            + '\x00'
            + base64.b64encode(file_name.encode('utf-8')).decode()
        ),
    }


@app.route('/download/<encrypted_file_id>', methods=['GET'])
async def download(encrypted_file_id: str):
    decrypted = aes.decrypt(encrypted_file_id).split('\x00')

    file_id, file_name = decrypted[0], base64.b64decode(decrypted[-1]).decode()
    file = await client.download_media(
        file_id,
        in_memory=True,
    )

    return send_file(
        io.BytesIO(file.getbuffer()),
        download_name=file_name,
    )


if __name__ == '__main__':
    threading.Thread(target=app.run, daemon=True).start()
    client.run()
