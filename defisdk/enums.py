from enum import Enum


class ActionType(Enum):
    Deposit = 1
    Withdraw = 2


class AmountType(Enum):
    Relative = 1
    Absolute = 2


class AdapterType(Enum):
    Asset = 1
    Debt = 2
