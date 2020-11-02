from typing import List, Union

from furl import furl

from defisdk.entities import AdapterBalance, ProtocolBalance, TokenBalance, TokenMetadata, AssetBalance
from defisdk.repositories.ethereum import BaseEthereumRepository
from defisdk.serializers import (
    defi_sdk_adapter_balances_to_entity,
    defi_sdk_protocol_balances_to_entity,
    defi_sdk_protocol_names_to_list_of_string,
    defi_sdk_token_adapter_names_to_list_of_string,
    defi_sdk_full_token_balance_to_entity
)
from defisdk.utils import get_signature_hash, hash_to_address, hash_to_list, remove_0x_prefix, string_to_hash


class DeFiSDKAPIRepository(BaseEthereumRepository):

    def __init__(self, ethereum_node_url: str, defisdk_registry: str):
        self._get_user_balance = get_signature_hash(b"getBalances(address)")
        self._get_adapter_balances = get_signature_hash(b"getAdapterBalances(address,address[])")
        self._get_protocol_balances = get_signature_hash(b"getProtocolBalances(address,string[])")
        self._get_protocol_names = get_signature_hash(b"getProtocolNames()")
        self._get_token_adapter_names = get_signature_hash(b"getTokenAdapterNames()")
        self._get_protocol_adapters = get_signature_hash(b"getProtocolAdapters(string)")
        self._get_token_adapter = get_signature_hash(b"getTokenAdapter(string)")
        self._get_full_token_balance = get_signature_hash(b"getFullTokenBalance(string,address)")
        self._get_final_full_token_balance = get_signature_hash(b"getFinalFullTokenBalance(string,address)")
        self._url = furl(ethereum_node_url)
        self._registry = defisdk_registry
        super().__init__()

    async def get_account_balance(
            self,
            address: str,
            block: Union[str, int] = 'latest'
    ) -> List[ProtocolBalance]:
        return await self._call(
            self._registry,
            self._get_user_balance + remove_0x_prefix(address).zfill(64),
            serializer=defi_sdk_protocol_balances_to_entity,
            block=block
        )

    async def get_adapter_balance(
            self,
            address: str,
            adapter: str,
            block: Union[str, int] = 'latest'
    ) -> AdapterBalance:
        words = [
            remove_0x_prefix(address).zfill(64),  # first argument: address
            remove_0x_prefix(hex(64)).zfill(64),  # position of the dynamic argument: [adapter]
            remove_0x_prefix(hex(1)).zfill(64),  # length of the dynamic argument: [adapter]
            remove_0x_prefix(adapter).zfill(64)  # second argument: [adapter]
        ]
        result = await self._call(
            self._registry,
            self._get_adapter_balances + ''.join(words),
            serializer=defi_sdk_adapter_balances_to_entity,
            block=block
        )
        return result[0]

    async def get_protocol_balance(
            self,
            address: str,
            protocol_name: str,
            block: Union[str, int] = 'latest'
    ) -> ProtocolBalance:
        words = [
            remove_0x_prefix(address).zfill(64),  # first argument: address
            remove_0x_prefix(hex(64)).zfill(64),  # position of the dynamic argument: [protocol[]]
            remove_0x_prefix(hex(1)).zfill(64),  # length of the dynamic argument: [protocol[]]
            remove_0x_prefix(hex(32)).zfill(64),  # position of the dynamic argument: [protocol]
            remove_0x_prefix(hex(len(protocol_name))).zfill(64),  # length of the dynamic argument: [protocol]
            remove_0x_prefix(string_to_hash(protocol_name)).ljust(64, '0')  # left-aligned argument
        ]
        result = await self._call(
            self._registry,
            self._get_protocol_balances + ''.join(words),
            serializer=defi_sdk_protocol_balances_to_entity,
            block=block
        )
        return result[0]

    async def get_protocol_names(
            self,
            block: Union[str, int] = 'latest'
    ) -> List[str]:
        return await self._call(
            self._registry,
            self._get_protocol_names,
            serializer=defi_sdk_protocol_names_to_list_of_string,
            block=block
        )

    async def get_token_adapter_names(
            self,
            block: Union[str, int] = 'latest'
    ) -> List[str]:
        return await self._call(
            self._registry,
            self._get_token_adapter_names,
            serializer=defi_sdk_token_adapter_names_to_list_of_string,
            block=block
        )

    async def get_protocol_adapter_names(
            self,
            protocol_name: str,
            block: Union[str, int] = 'latest'
    ) -> List[str]:
        words = [
            remove_0x_prefix(hex(32)).zfill(64),  # position of the dynamic argument
            remove_0x_prefix(hex(len(protocol_name))).zfill(64),  # length of the dynamic argument
            remove_0x_prefix(string_to_hash(protocol_name)).ljust(64, '0')  # left-aligned argument
        ]
        return await self._call(
            self._registry,
            self._get_protocol_adapters + ''.join(words),
            serializer=hash_to_list,
            block=block
        )

    async def get_token_adapter(
            self,
            token_adapter_name: str,
            block: Union[str, int] = 'latest'
    ) -> str:
        words = [
            remove_0x_prefix(hex(32)).zfill(64),  # position of the dynamic argument
            remove_0x_prefix(hex(len(token_adapter_name))).zfill(64),  # length of the dynamic argument
            remove_0x_prefix(string_to_hash(token_adapter_name)).ljust(64, '0')  # left-aligned argument
        ]
        return await self._call(
            self._registry,
            self._get_token_adapter + ''.join(words),
            serializer=hash_to_address,
            block=block
        )

    async def get_full_token_balance(
            self,
            token_type: str,
            token_address: str,
            block: Union[str, int] = 'latest'
    ) -> AssetBalance:
        words = [
            remove_0x_prefix(hex(64)).zfill(64),  # position of the dynamic argument
            remove_0x_prefix(token_address).zfill(64),  # second argument: address
            remove_0x_prefix(hex(len(bytes(token_type, 'utf-8')))).zfill(64),  # length of the dynamic argument
            remove_0x_prefix(string_to_hash(token_type)).ljust(64, '0')  # left-aligned argument
        ]
        return await self._call(
            self._registry,
            self._get_full_token_balance + ''.join(words),
            serializer=defi_sdk_full_token_balance_to_entity,
            block=block
        )

    async def get_final_full_token_balance(
            self,
            token_type: str,
            token_address: str,
            block: Union[str, int] = 'latest'
    ) -> AssetBalance:
        words = [
            remove_0x_prefix(hex(64)).zfill(64),  # position of the dynamic argument
            remove_0x_prefix(token_address).zfill(64),  # second argument: address
            remove_0x_prefix(hex(len(bytes(token_type, 'utf-8')))).zfill(64),  # length of the dynamic argument
            remove_0x_prefix(string_to_hash(token_type)).ljust(64, '0')  # left-aligned argument
        ]
        return await self._call(
            self._registry,
            self._get_final_full_token_balance + ''.join(words),
            serializer=defi_sdk_full_token_balance_to_entity,
            block=block
        )

    async def get_token_components(
            self,
            token_type: str,
            token_address: str,
            block: Union[str, int] = 'latest'
    ) -> List[TokenBalance]:
        full_token_balance = await self.get_full_token_balance(token_type, token_address, block)
        return full_token_balance.underlying_token_balances

    async def get_final_token_components(
            self,
            token_type: str,
            token_address: str,
            block: Union[str, int] = 'latest'
    ) -> List[TokenBalance]:
        full_token_balance = await self.get_final_full_token_balance(token_type, token_address, block)
        return full_token_balance.underlying_token_balances

    async def get_token_metadata(
            self,
            token_type: str,
            token_address: str,
            block: Union[str, int] = 'latest'
    ) -> TokenMetadata:
        full_token_balance = await self.get_full_token_balance(token_type, token_address, block)
        return full_token_balance.base_token_balance.metadata
