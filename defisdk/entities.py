from dataclasses import dataclass
from decimal import Decimal
from typing import List


@dataclass(eq=True, frozen=True)
class TokenMetadata:
    address: str
    name: str
    symbol: str
    decimals: int


@dataclass(eq=True, frozen=True)
class TokenBalance:
    metadata: TokenMetadata
    balance: Decimal


@dataclass(eq=True, frozen=True)
class AssetBalance:
    base_token_balance: TokenBalance
    underlying_token_balances: List[TokenBalance]


@dataclass(eq=True, frozen=True)
class AdapterMetadata:
    address: str
    type: str


@dataclass(eq=True, frozen=True)
class AdapterBalance:
    metadata: AdapterMetadata
    asset_balances: List[AssetBalance]


@dataclass(eq=True, frozen=True)
class ProtocolMetadata:
    name: str
    description: str
    website_url: str
    icon_url: str
    version: int


@dataclass(eq=True, frozen=True)
class ProtocolBalance:
    metadata: ProtocolMetadata
    adapter_balances: List[AdapterBalance]
