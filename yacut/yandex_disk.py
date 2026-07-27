import asyncio

import aiohttp


UPLOAD_LINK_URL = (
    'https://cloud-api.yandex.net/v1/disk/resources/upload'
)
DOWNLOAD_LINK_URL = (
    'https://cloud-api.yandex.net/v1/disk/resources/download'
)


async def upload_file(session, filename, content):
    disk_path = f'app:/{filename}'

    async with session.get(
        UPLOAD_LINK_URL,
        params={
            'path': disk_path,
            'overwrite': 'true',
        },
    ) as response:
        response.raise_for_status()
        upload_url = (await response.json())['href']

    async with session.put(upload_url, data=content) as response:
        response.raise_for_status()

    async with session.get(
        DOWNLOAD_LINK_URL,
        params={'path': disk_path},
    ) as response:
        response.raise_for_status()
        download_url = (await response.json())['href']

    return filename, download_url


async def upload_files(files, token):
    prepared_files = [
        (file.filename, file.read())
        for file in files
    ]

    headers = {
        'Authorization': f'OAuth {token}',
    }

    async with aiohttp.ClientSession(headers=headers) as session:
        tasks = [
            upload_file(session, filename, content)
            for filename, content in prepared_files
        ]
        return await asyncio.gather(*tasks)