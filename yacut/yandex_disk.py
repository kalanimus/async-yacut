from __future__ import annotations

import asyncio
from typing import Any

import aiohttp

UPLOAD_LINK_URL: str = (
    'https://cloud-api.yandex.net/v1/disk/resources/upload'
)
DOWNLOAD_LINK_URL: str = (
    'https://cloud-api.yandex.net/v1/disk/resources/download'
)


async def upload_file(
    session: aiohttp.ClientSession,
    filename: str,
    content: bytes,
) -> tuple[str, str]:
    """Upload a single file to Yandex Disk and return download URL."""
    disk_path: str = f'app:/{filename}'

    async with session.get(
        UPLOAD_LINK_URL,
        params={
            'path': disk_path,
            'overwrite': 'true',
        },
    ) as response:
        response.raise_for_status()
        data: dict[str, Any] = await response.json()
        upload_url: str = data['href']

    async with session.put(upload_url, data=content) as response:
        response.raise_for_status()

    async with session.get(
        DOWNLOAD_LINK_URL,
        params={'path': disk_path},
    ) as response:
        response.raise_for_status()
        data = await response.json()
        download_url: str = data['href']

    return filename, download_url


async def upload_files(
    files: list[Any],
    token: str | None,
) -> list[tuple[str, str]]:
    """Upload multiple files to Yandex Disk concurrently."""
    if not token:
        return []

    prepared_files: list[tuple[str, bytes]] = [
        (file.filename, file.read())
        for file in files
    ]

    headers: dict[str, str] = {
        'Authorization': f'OAuth {token}',
    }

    async with aiohttp.ClientSession(headers=headers) as session:
        tasks: list[asyncio.Task[tuple[str, str]]] = [
            upload_file(session, filename, content)
            for filename, content in prepared_files
        ]
        return await asyncio.gather(*tasks)
