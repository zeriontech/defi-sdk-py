from dataclasses import dataclass, field
from decimal import Decimal
from typing import List

from .constants import ZERO_ADDRESS


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


@dataclass(frozen=True)
class TokenAmount:
    token: str = ZERO_ADDRESS
    amount: int = 0
    amount_type: int = 0

    def encode(self):
        return [
            self.token,
            self.amount,
            self.amount_type,
        ]


@dataclass(frozen=True)
class AbsoluteTokenAmount:
    token: str = ZERO_ADDRESS
    absolute_amount: int = 0

    def encode(self):
        return [
            self.token,
            self.absolute_amount,
        ]


@dataclass(frozen=True)
class Fee:
    share: int = 0
    beneficiary: str = ZERO_ADDRESS

    def encode(self):
        return [
            self.share,
            self.beneficiary,
        ]


@dataclass(frozen=True)
class Action:
    action_type: int = 0
    protocol_adapter_id: str = ''
    tokenAmounts: List[TokenAmount] = field(default_factory=list)
    data: str = ''

    def encode(self):
        return [
            self.protocol_adapter_id,
            self.action_type,
            [x.encode() for x in self.tokenAmounts],
            self.data,
        ]
