from socket import AF_INET
from typing import Optional

import aiohttp
from fastapi.logger import logger

fastAPI_logger = logger

SIZE_POOL_AIOHTTP = 100


class AiohttpClient:
    aiohttp_client: Optional[aiohttp.ClientSession] = None

    @classmethod
    def get_aiohttp_client(cls) -> aiohttp.ClientSession:
        if cls.aiohttp_client is None:
            timeout = aiohttp.ClientTimeout(total=100)
            connector = aiohttp.TCPConnector(family=AF_INET, limit_per_host=SIZE_POOL_AIOHTTP)
            cls.aiohttp_client = aiohttp.ClientSession(timeout=timeout, connector=connector)

        return cls.aiohttp_client

    @classmethod
    async def close_aiohttp_client(cls) -> None:
        if cls.aiohttp_client:
            await cls.aiohttp_client.close()
            cls.aiohttp_client = None

    @classmethod
    async def post(cls, url: str, params=None):
        client = cls.get_aiohttp_client()

        async with client.post(url, json=params) as response:
            if response.status >= 400:
                return {"ERROR OCCURED" + str(await response.text())}

            json_result = await response.json()

        return json_result

    @classmethod
    async def get(cls, url: str, ssl: Optional[bool], params: Optional[str] = None):
        client = cls.get_aiohttp_client()

        async with client.get(url, ssl=ssl, params=params) as response:
            if response.status >= 400:
                return {"ERROR OCCURED" + str(await response.text())}

            json_result = await response.json()

        return json_result
