from typing import List

from defisdk.entities import (
    AdapterBalance, AdapterMetadata, AssetBalance, ProtocolBalance, ProtocolMetadata, TokenBalance, TokenMetadata
)
from defisdk.utils import (
    hash_to_address, hash_to_decimal, hash_to_int, hash_to_list, hash_to_words, words_to_list, words_to_string
)


def defi_sdk_token_metadata_to_entity(words: List[str]) -> TokenMetadata:
    name_location = hash_to_int(words[1]) // 32
    symbol_location = hash_to_int(words[2]) // 32
    return TokenMetadata(
        address=hash_to_address(words[0]),
        name=words_to_string(words[name_location:symbol_location]),
        symbol=words_to_string(words[symbol_location:]),
        decimals=hash_to_int(words[3])
    )


def defi_sdk_token_balance_to_entity(
        words: List[str],
        rate: bool = False,
        base_token_decimals: int = 18
) -> TokenBalance:
    metadata_location = hash_to_int(words[0]) // 32
    metadata = defi_sdk_token_metadata_to_entity(words[metadata_location:])
    decimal_shift = 18 - base_token_decimals if rate else 0
    return TokenBalance(
        metadata=metadata,
        balance=hash_to_decimal(words[1], metadata.decimals + decimal_shift)
    )


def defi_sdk_asset_balance_to_entity(words: List[str], rate: bool = False) -> AssetBalance:
    base_location = hash_to_int(words[0]) // 32
    underlying_location = hash_to_int(words[1]) // 32
    base_balance = defi_sdk_token_balance_to_entity(words[base_location:underlying_location], rate=rate)
    underlying_balances = words_to_list(
        words[underlying_location:],
        lambda x: defi_sdk_token_balance_to_entity(x, rate=rate, base_token_decimals=base_balance.metadata.decimals),
        True
    )
    return AssetBalance(
        base_token_balance=base_balance,
        underlying_token_balances=underlying_balances
    )


def defi_sdk_adapter_metadata_to_entity(words: List[str]) -> AdapterMetadata:
    type_location = hash_to_int(words[1]) // 32
    return AdapterMetadata(
        address=hash_to_address(words[0]),
        type=words_to_string(words[type_location:])
    )


def defi_sdk_adapter_balance_to_entity(words: List[str]) -> AdapterBalance:
    metadata_location = hash_to_int(words[0]) // 32
    balances_location = hash_to_int(words[1]) // 32
    metadata = defi_sdk_adapter_metadata_to_entity(words[metadata_location:balances_location])
    balances = words_to_list(words[balances_location:], defi_sdk_asset_balance_to_entity, True)
    return AdapterBalance(
        metadata=metadata,
        asset_balances=balances
    )


def defi_sdk_protocol_metadata_to_entity(words: List[str]) -> ProtocolMetadata:
    name_location = hash_to_int(words[0]) // 32
    description_location = hash_to_int(words[1]) // 32
    website_url_location = hash_to_int(words[2]) // 32
    icon_url_location = hash_to_int(words[3]) // 32
    return ProtocolMetadata(
        name=words_to_string(words[name_location:description_location]),
        description=words_to_string(words[description_location:website_url_location]),
        website_url=words_to_string(words[website_url_location:icon_url_location]),
        icon_url=words_to_string(words[icon_url_location:]),
        version=hash_to_int(words[4])
    )


def defi_sdk_protocol_balance_to_entity(words: List[str]) -> ProtocolBalance:
    metadata_location = hash_to_int(words[0]) // 32
    balances_location = hash_to_int(words[1]) // 32
    metadata = defi_sdk_protocol_metadata_to_entity(words[metadata_location:balances_location])
    balances = words_to_list(words[balances_location:], defi_sdk_adapter_balance_to_entity, True)
    return ProtocolBalance(
        metadata=metadata,
        adapter_balances=balances
    )


def defi_sdk_protocol_balances_to_entity(data: str) -> List[ProtocolBalance]:
    return hash_to_list(data, defi_sdk_protocol_balance_to_entity, dynamic_elements=True)


def defi_sdk_adapter_balances_to_entity(data: str) -> List[AdapterBalance]:
    return hash_to_list(data, defi_sdk_adapter_balance_to_entity, dynamic_elements=True)


def defi_sdk_token_adapter_names_to_list_of_string(data: str) -> List[str]:
    return hash_to_list(data, words_to_string, dynamic_elements=True)


def defi_sdk_protocol_names_to_list_of_string(data: str) -> List[str]:
    return hash_to_list(data, words_to_string, dynamic_elements=True)


def defi_sdk_full_token_balance_to_entity(data: str) -> AssetBalance:
    return defi_sdk_asset_balance_to_entity(hash_to_words(data)[1:], rate=True)
