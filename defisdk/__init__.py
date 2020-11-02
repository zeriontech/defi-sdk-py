from typing import List, Union

from .entities import AdapterBalance, AssetBalance, ProtocolBalance, TokenBalance, TokenMetadata
from .repositories import DeFiSDKAPIRepository
from .settings import DEFI_SDK_REGISTRY


class DeFiSDK:

    def __init__(self, ethereum_node_url: str, defisdk_registry: str = DEFI_SDK_REGISTRY):
        self._repository = DeFiSDKAPIRepository(ethereum_node_url, defisdk_registry=defisdk_registry)

    async def get_account_balance(
            self,
            address: str,
            block: Union[str, int] = 'latest'
    ) -> List[ProtocolBalance]:
        return await self._repository.get_account_balance(address, block)

    async def get_adapter_balance(
            self,
            address: str,
            adapter: str,
            block: Union[str, int] = 'latest'
    ) -> AdapterBalance:
        return await self._repository.get_adapter_balance(address, adapter, block)

    async def get_protocol_balance(
            self,
            address: str,
            protocol_name: str,
            block: Union[str, int] = 'latest'
    ) -> ProtocolBalance:
        return await self._repository.get_protocol_balance(address, protocol_name, block)

    async def get_protocol_names(
            self,
            block: Union[str, int] = 'latest'
    ) -> List[str]:
        return await self._repository.get_protocol_names(block)

    async def get_token_adapter_names(
            self,
            block: Union[str, int] = 'latest'
    ) -> List[str]:
        return await self._repository.get_token_adapter_names(block)

    async def get_protocol_adapter_names(
            self,
            protocol_name: str,
            block: Union[str, int] = 'latest'
    ) -> List[str]:
        return await self._repository.get_protocol_adapter_names(protocol_name, block)

    async def get_token_adapter(
            self,
            token_adapter_name: str,
            block: Union[str, int] = 'latest'
    ) -> str:
        return await self._repository.get_token_adapter(token_adapter_name, block)

    async def get_full_token_balance(
            self,
            token_type: str,
            token_address: str,
            block: Union[str, int] = 'latest'
    ) -> AssetBalance:
        return await self._repository.get_full_token_balance(token_type, token_address, block)

    async def get_final_full_token_balance(
            self,
            token_type: str,
            token_address: str,
            block: Union[str, int] = 'latest'
    ) -> AssetBalance:
        return await self._repository.get_final_full_token_balance(token_type, token_address, block)

    async def get_token_components(
            self,
            token_type: str,
            token_address: str,
            block: Union[str, int] = 'latest'
    ) -> List[TokenBalance]:
        return await self._repository.get_token_components(token_type, token_address, block)

    async def get_final_token_components(
            self,
            token_type: str,
            token_address: str,
            block: Union[str, int] = 'latest'
    ) -> List[TokenBalance]:
        return await self._repository.get_final_token_components(token_type, token_address, block)

    async def get_token_metadata(
            self,
            token_type: str,
            token_address: str,
            block: Union[str, int] = 'latest'
    ) -> TokenMetadata:
        return await self._repository.get_token_metadata(token_type, token_address, block)
