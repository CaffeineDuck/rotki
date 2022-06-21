from rotkehlchen.chain.ethereum.types import string_to_ethereum_address
from rotkehlchen.types import Timestamp, deserialize_evm_tx_hash

RANGE_PREFIX_ETHTX = 'ethtxs'
RANGE_PREFIX_ETHINTERNALTX = 'ethinternaltxs'
RANGE_PREFIX_ETHTOKENTX = 'ethtokentxs'

MODULES_PACKAGE = 'rotkehlchen.chain.ethereum.modules'
MODULES_PREFIX = MODULES_PACKAGE + '.'
MODULES_PREFIX_LENGTH = len(MODULES_PREFIX)

ZERO_ADDRESS = string_to_ethereum_address('0x0000000000000000000000000000000000000000')
GENESIS_HASH = deserialize_evm_tx_hash('0x' + '0' * 64)  # hash for transactions in genesis block
ETHEREUM_BEGIN = Timestamp(1438269973)

CPT_KRAKEN = 'kraken'
