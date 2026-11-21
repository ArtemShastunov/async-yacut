import asyncio

import aiohttp
from flask import current_app

from yacut.constants import YANDEX_DISK_API_URL


async def get_upload_link(session, headers, path):
    url = f'{YANDEX_DISK_API_URL}/upload'
    params = {'path': path, 'overwrite': 'True'}
    async with session.get(
        url, headers=headers, params=params
    ) as response:
        data = await response.json()
        return data['href']


async def upload_file_to_disk(session, token, file):
    headers = {'Authorization': f'OAuth {token}'}
    path = 'app:/' + file.filename

    upload_href = await get_upload_link(session, headers, path)

    async with session.put(
        upload_href, data=file.read()
    ) as response:
        pass

    download_url = f'{YANDEX_DISK_API_URL}/download'
    params = {'path': path}
    async with session.get(
        download_url, headers=headers, params=params
    ) as response:
        data = await response.json()
        return file.filename, data['href']


async def upload_files_to_disk(files):
    token = current_app.config['DISK_TOKEN']
    async with aiohttp.ClientSession() as session:
        tasks = [upload_file_to_disk(session, token, file) for file in files]
        return await asyncio.gather(*tasks)
