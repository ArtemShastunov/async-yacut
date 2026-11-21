import asyncio

import aiohttp
from flask import current_app


async def get_upload_link(session, headers, path):
    """Получает временную ссылку для загрузки файла на Диск."""
    url = (
        'https://cloud-api.yandex.net/v1/disk/resources/upload'
    )
    params = {'path': path, 'overwrite': 'True'}
    async with session.get(
        url, headers=headers, params=params
    ) as response:
        data = await response.json()
        return data['href']


async def upload_file_to_disk(session, token, file):
    """Загружает файл на Диск и возвращает прямую ссылку."""
    headers = {'Authorization': f'OAuth {token}'}
    path = 'app:/' + file.filename

    upload_href = await get_upload_link(session, headers, path)

    async with session.put(upload_href, data=file.read()) as response:
        pass

    download_url = (
        'https://cloud-api.yandex.net/v1/disk/resources/download'
    )
    params = {'path': path}
    async with session.get(
        download_url, headers=headers, params=params
    ) as response:
        data = await response.json()
        return file.filename, data['href']


async def upload_files_to_disk(files):
    """Запускает параллельную загрузку всех переданных файлов."""
    token = current_app.config['DISK_TOKEN']

    async with aiohttp.ClientSession() as session:
        tasks = [upload_file_to_disk(session, token, file) for file in files]
        results = await asyncio.gather(*tasks)

    return results
