# DeFiSDK.py

This library is a simple asynchronous python wrapper around [DeFi SDK](https://github.com/zeriontech/defi-sdk).

# Installation
```bash
$ pip3 install defisdk
```

# Usage

### Initialize DeFiSDK
```python
from defisdk import DeFiSDK

INFURA_API_KEY = '<MY API KEY>'
ETHEREUM_NODE_URL = f'https://mainnet.infura.io/v3/{INFURA_API_KEY}'

defi_sdk = DeFiSDK(ETHEREUM_NODE_URL)
```

### Get supported protocols

```python
>>> await defi_sdk.get_protocol_names()
['PieDAO',
 'Multi-Collateral Dai',
 'Bancor',
 'DeFi Money Market',
 'TokenSets',
 '0x Staking',
 'Uniswap V1',
 'Synthetix',
 'PoolTogether',
 'Dai Savings Rate',
 'Chai',
 'iearn.finance (v3)',
 'iearn.finance (v2)',
 'Idle',
 'dYdX',
 'Curve',
 'Compound',
 'Balancer',
 'Aave']
```


### Get supported token types

```python
>>> await defi_sdk.get_token_adapter_names()
['PieDAO Pie Token',
 'SmartToken',
 'MToken',
 'SetToken',
 'Uniswap V1 pool token',
 'PoolTogether pool',
 'Chai token',
 'YToken',
 'IdleToken',
 'Curve pool token',
 'CToken',
 'Balancer pool token',
 'AToken',
 'ERC20']
```

### Get derivative token underlying components

```python
>>> UNISWAP_DAI_POOL = '0x2a1530c4c41db0b0b2bb646cb5eb1a67b7158667'
>>> await defi_sdk.get_token_components('Uniswap V1 pool token', UNISWAP_DAI_POOL)
[
    TokenBalance(
        metadata=TokenMetadata(
            address='0xeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee',
            name='Ether',
            symbol='ETH',
            decimals=18
        ),
        balance=Decimal('1.115069671320704604')
    ),
    TokenBalance(
        metadata=TokenMetadata(
            address='0x6b175474e89094c44da98b954eedeac495271d0f',
            name='Dai Stablecoin',
            symbol='DAI',
            decimals=18
        ),
        balance=Decimal('216.692050327076500045')
    )
]
```

### Get account balance locked in a protocol

```python
>>> USER_ADDRESS = '0xa218a8346454c982912cf6d14c714663c2d510d8'
>>> await defi_sdk.get_protocol_balance(USER_ADDRESS, 'Aave')
ProtocolBalance(
    metadata=ProtocolMetadata(
        name='Aave',
        description='Decentralized lending & borrowing protocol',
        website_url='aave.com',
        icon_url='protocol-icons.s3.amazonaws.com/aave.png',
        version=0
    ),
    adapter_balances=[
        AdapterBalance(
            metadata=AdapterMetadata(
                address='0x8b62c02091fe06ae3454d3c12921b32611ba5501',
                type='Asset'
            ),
            asset_balances=[
                AssetBalance(
                    base_token_balance=TokenBalance(
                        metadata=TokenMetadata(
                            address='0xfc1e690f61efd961294b3e1ce3313fbd8aa4f85d',
                            name='Aave Interest bearing DAI',
                            symbol='aDAI',
                            decimals=18
                        ),
                        balance=Decimal('1.006384746516743708')
                    ),
                    underlying_token_balances=[
                        TokenBalance(
                            metadata=TokenMetadata(
                                address='0x6b175474e89094c44da98b954eedeac495271d0f',
                                name='Dai Stablecoin',
                                symbol='DAI',
                                decimals=18
                            ),
                            balance=Decimal('1.006384746516743708')
                        )
                    ]
                )
            ]
        )
    ]
)
```

### Get account balance across all the support protocols

```python
>>> USER_ADDRESS = '0xa218a8346454c982912cf6d14c714663c2d510d8'
>>> await defi_sdk.get_account_balance(USER_ADDRESS)
[
    ProtocolBalance(
        metadata=ProtocolMetadata(
            name='Synthetix',
            description='Synthetic assets protocol',
            website_url='synthetix.io',
            icon_url='protocol-icons.s3.amazonaws.com/synthetix.png',
            version=1
        ),
        adapter_balances=[
            AdapterBalance(
                metadata=AdapterMetadata(
                    address='0xfd23f77fbd9fc08c4634cc3fdd58054cece3792b',
                    type='Asset'
                ),
                asset_balances=[
                    AssetBalance(
                        base_token_balance=TokenBalance(
                            metadata=TokenMetadata(
                                address='0xc011a73ee8576fb46f5e1c5751ca3b9fe0af2a6f',
                                name='Synthetix Network Token',
                                symbol='SNX',
                                decimals=18
                            ),
                            balance=Decimal('0.010000000000000000')
                        ),
                        underlying_token_balances=[]
                    )
                ]
            )
        ]
    ),
    ProtocolBalance(
        metadata=ProtocolMetadata(
            name='dYdX',
            description='Decentralized trading platform',
            website_url='dydx.exchange',
            icon_url='protocol-icons.s3.amazonaws.com/dYdX.png',
            version=0
        ),
        adapter_balances=[
            AdapterBalance(
                metadata=AdapterMetadata(
                    address='0x375c3222bb7d4834b4381abd4ed15dff4d4c0a68',
                    type='Asset'
                ),
                asset_balances=[
                    AssetBalance(
                        base_token_balance=TokenBalance(
                            metadata=TokenMetadata(
                                address='0xc02aaa39b223fe8d0a0e5c4f27ead9083c756cc2',
                                name='Wrapped Ether',
                                symbol='WETH',
                                decimals=18
                            ),
                            balance=Decimal('0.185594562946597852')
                        ),
                        underlying_token_balances=[]
                    ),
                    AssetBalance(
                        base_token_balance=TokenBalance(
                            metadata=TokenMetadata(
                                address='0x6b175474e89094c44da98b954eedeac495271d0f',
                                name='Dai Stablecoin',
                                symbol='DAI',
                                decimals=18
                            ),
                            balance=Decimal('185.230336031983831471')
                        ),
                        underlying_token_balances=[]
                    )
                ]
            ),
            AdapterBalance(
                metadata=AdapterMetadata(
                    address='0xbf3fc291876707b2d0c8fc49bcd76fae00219d37',
                    type='Debt'
                ),
                asset_balances=[
                    AssetBalance(
                        base_token_balance=TokenBalance(
                            metadata=TokenMetadata(
                                address='0xa0b86991c6218b36c1d19d4a2e9eb0ce3606eb48',
                                name='USD//C',
                                symbol='USDC',
                                decimals=6
                            ),
                            balance=Decimal('50.819863')
                        ),
                        underlying_token_balances=[]
                    )
                ]
            )
        ]
    ),
    ProtocolBalance(
        metadata=ProtocolMetadata(
            name='Compound',
            description='Decentralized lending & borrowing protocol',
            website_url='compound.finance',
            icon_url='protocol-icons.s3.amazonaws.com/compound.png',
            version=0
        ),
        adapter_balances=[
            AdapterBalance(
                metadata=AdapterMetadata(
                    address='0xaa74b0f33cab1b291980532bc5e0057e10adb2a3',
                    type='Asset'
                ),
                asset_balances=[
                    AssetBalance(
                        base_token_balance=TokenBalance(
                            metadata=TokenMetadata(
                                address='0x4ddc2d193948926d02f9b1fe9e1daa0718270ed5',
                                name='Compound Ether',
                                symbol='cETH',
                                decimals=8
                            ),
                            balance=Decimal('499.72749958')
                        ),
                        underlying_token_balances=[
                            TokenBalance(
                                metadata=TokenMetadata(
                                    address='0xeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee',
                                    name='Ether',
                                    symbol='ETH',
                                    decimals=18
                                ),
                                balance=Decimal('10.000492390829125770')
                            )
                        ]
                    ),
                    AssetBalance(
                        base_token_balance=TokenBalance(
                            metadata=TokenMetadata(
                                address='0x39aa39c021dfbae8fac545936693ac917d5e7563',
                                name='Compound USD Coin',
                                symbol='cUSDC',
                                decimals=8
                            ),
                            balance=Decimal('48.61414113')
                        ),
                        underlying_token_balances=[
                            TokenBalance(
                                metadata=TokenMetadata(
                                    address='0xa0b86991c6218b36c1d19d4a2e9eb0ce3606eb48',
                                    name='USD//C',
                                    symbol='USDC',
                                    decimals=6
                                ),
                                balance=Decimal('1.021851')
                            )
                        ]
                    )
                ]
            ),
            AdapterBalance(
                metadata=AdapterMetadata(
                    address='0xae61b0d0a562e5c1daf9c1ded4a8fd6a770b639a',
                    type='Debt'
                ),
                asset_balances=[
                    AssetBalance(
                        base_token_balance=TokenBalance(
                            metadata=TokenMetadata(
                                address='0x0d8775f648430679a709e98d2b0cb6250d2887ef',
                                name='Basic Attention Token',
                                symbol='BAT', decimals=18
                            ),
                            balance=Decimal('0.000117145388391941')
                        ),
                        underlying_token_balances=[]
                    ),
                    AssetBalance(
                        base_token_balance=TokenBalance(
                            metadata=TokenMetadata(
                                address='0xa0b86991c6218b36c1d19d4a2e9eb0ce3606eb48',
                                name='USD//C',
                                symbol='USDC',
                                decimals=6
                            ),
                            balance=Decimal('437.598211')
                        ),
                        underlying_token_balances=[]
                    )
                ]
            )
        ]
    ),
    ProtocolBalance(
        metadata=ProtocolMetadata(
            name='Aave',
            description='Decentralized lending & borrowing protocol',
            website_url='aave.com',
            icon_url='protocol-icons.s3.amazonaws.com/aave.png',
            version=0
        ),
        adapter_balances=[
            AdapterBalance(
                metadata=AdapterMetadata(
                    address='0x8b62c02091fe06ae3454d3c12921b32611ba5501',
                    type='Asset'
                ),
                asset_balances=[
                    AssetBalance(
                        base_token_balance=TokenBalance(
                            metadata=TokenMetadata(
                                address='0xfc1e690f61efd961294b3e1ce3313fbd8aa4f85d',
                                name='Aave Interest bearing DAI',
                                symbol='aDAI',
                                decimals=18
                            ),
                            balance=Decimal('1.006383863871752377')
                        ),
                        underlying_token_balances=[
                            TokenBalance(
                                metadata=TokenMetadata(
                                    address='0x6b175474e89094c44da98b954eedeac495271d0f',
                                    name='Dai Stablecoin',
                                    symbol='DAI',
                                    decimals=18
                                ),
                                balance=Decimal('1.006383863871752377')
                            )
                        ]
                    )
                ]
            )
        ]
    )
]
```
