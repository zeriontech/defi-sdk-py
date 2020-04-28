import aiohttp

from typing import Any, Dict
from furl import furl


class BaseAPIRepository:
    _url: furl

    @property
    def url(self):
        return self._url.copy()

    @staticmethod
    async def _post(url: str, headers: Dict[str, str], data: Dict[str, Any]) -> Dict[str, Any]:
        async with aiohttp.ClientSession(headers=headers) as session:
            async with session.post(url, json=data) as r:
                return await r.json()
