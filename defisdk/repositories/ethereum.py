import itertools
from typing import Any, Dict, List, Optional

from defisdk.errors import EthereumNodeEmptyResponse, EthereumNodeNoResponse, EthereumNodeResponseException
from defisdk.repositories.base import BaseAPIRepository
from defisdk.utils import represent_address


class BaseEthereumRepository(BaseAPIRepository):

    def __init__(self, *args, **kwargs):
        self.request_counter = itertools.count()

    def prepare_rpc_request_body(self, method: str, params: Optional[List] = None) -> Dict[str, Any]:
        params = params or []
        return {"jsonrpc": "2.0", "method": method, "params": params or [], "id": next(self.request_counter)}

    async def call_method(self, method: str, params: Optional[List] = None) -> Optional[Dict[str, Any]]:
        headers = {'Content-Type': 'application/json'}
        data = self.prepare_rpc_request_body(method, params)
        node_answer = None

        try:
            node_answer = await self._post(url=self.url.url, headers=headers, data=data)
        except Exception as e:
            raise EthereumNodeResponseException(params, e.message, e.code, e.response)
        finally:
            if not node_answer.get('result'):
                raise EthereumNodeNoResponse(node_answer)
            if node_answer['result'] == '0x':
                raise EthereumNodeEmptyResponse()
            if node_answer and 'error' in node_answer:
                raise EthereumNodeResponseException(
                    params, node_answer['error']['message'], node_answer['error']['code'], None
                )

        return node_answer

    async def _call(self, _to: str, data: str, serializer=lambda x: x, block='latest'):
        block = hex(block) if isinstance(block, int) else block
        params = [{'to': represent_address(_to), 'data': data}, block]
        node_answer = await self.call_method('eth_call', params)
        return serializer(node_answer['result'])
