import pytest

from rotkehlchen.accounting.structures.balance import Balance
from rotkehlchen.accounting.structures.base import (
    HistoryBaseEntry,
    HistoryEventSubType,
    HistoryEventType,
)
from rotkehlchen.chain.ethereum.modules.compound.constants import CPT_COMPOUND
from rotkehlchen.constants.assets import A_CETH, A_COMP, A_ETH
from rotkehlchen.constants.misc import ZERO
from rotkehlchen.fval import FVal
from rotkehlchen.tests.utils.ethereum import get_decoded_events_of_transaction
from rotkehlchen.types import Location, deserialize_evm_tx_hash

ADDY = '0x5727c0481b90a129554395937612d8b9301D6c7b'


@pytest.mark.parametrize('ethereum_accounts', [[ADDY]])  # noqa: E501
def test_compound_ether_deposit(database, ethereum_manager, function_scope_messages_aggregator):
    """Data taken from:
    https://etherscan.io/tx/0x06a8b9f758b0471886186c2a48dea189b3044916c7f94ee7f559026fefd91c39
    """
    # TODO: For faster tests hard-code the transaction and the logs here so no remote query needed
    tx_hash = deserialize_evm_tx_hash('0x06a8b9f758b0471886186c2a48dea189b3044916c7f94ee7f559026fefd91c39')  # noqa: E501
    events = get_decoded_events_of_transaction(
        ethereum_manager=ethereum_manager,
        database=database,
        msg_aggregator=function_scope_messages_aggregator,
        tx_hash=tx_hash,
    )
    expected_events = [
        HistoryBaseEntry(
            event_identifier=tx_hash.hex(),  # pylint: disable=no-member
            sequence_index=0,
            timestamp=1598639099000,
            location=Location.BLOCKCHAIN,
            event_type=HistoryEventType.SPEND,
            event_subtype=HistoryEventSubType.FEE,
            asset=A_ETH,
            balance=Balance(amount=FVal('0.014122318'), usd_value=ZERO),
            location_label=ADDY,
            notes=f'Burned 0.014122318 ETH in gas from {ADDY}',
            counterparty='gas',
        ), HistoryBaseEntry(
            event_identifier=tx_hash.hex(),  # pylint: disable=no-member
            sequence_index=1,
            timestamp=1598639099000,
            location=Location.BLOCKCHAIN,
            event_type=HistoryEventType.DEPOSIT,
            event_subtype=HistoryEventSubType.DEPOSIT_ASSET,
            asset=A_ETH,
            balance=Balance(amount=FVal('0.5'), usd_value=ZERO),
            location_label=ADDY,
            notes='Deposit 0.5 ETH to compound',
            counterparty=CPT_COMPOUND,
        ), HistoryBaseEntry(
            event_identifier=tx_hash.hex(),  # pylint: disable=no-member
            sequence_index=33,
            timestamp=1598639099000,
            location=Location.BLOCKCHAIN,
            event_type=HistoryEventType.RECEIVE,
            event_subtype=HistoryEventSubType.RECEIVE_WRAPPED,
            asset=A_CETH,
            balance=Balance(amount=FVal('24.97649991'), usd_value=ZERO),
            location_label=ADDY,
            notes='Receive 24.97649991 cETH from compound',
            counterparty=CPT_COMPOUND,
        )]
    assert events == expected_events


@pytest.mark.parametrize('ethereum_accounts', [[ADDY]])  # noqa: E501
def test_compound_ether_withdraw(database, ethereum_manager, function_scope_messages_aggregator):
    """Data taken from:
    https://etherscan.io/tx/0x024bd402420c3ba2f95b875f55ce2a762338d2a14dac4887b78174254c9ab807
    """
    # TODO: For faster tests hard-code the transaction and the logs here so no remote query needed
    tx_hash = deserialize_evm_tx_hash('0x024bd402420c3ba2f95b875f55ce2a762338d2a14dac4887b78174254c9ab807')  # noqa: E501
    events = get_decoded_events_of_transaction(
        ethereum_manager=ethereum_manager,
        database=database,
        msg_aggregator=function_scope_messages_aggregator,
        tx_hash=tx_hash,
    )
    expected_events = [
        HistoryBaseEntry(
            event_identifier=tx_hash.hex(),  # pylint: disable=no-member
            sequence_index=0,
            timestamp=1598813490000,
            location=Location.BLOCKCHAIN,
            event_type=HistoryEventType.SPEND,
            event_subtype=HistoryEventSubType.FEE,
            asset=A_ETH,
            balance=Balance(amount=FVal('0.02858544'), usd_value=ZERO),
            location_label=ADDY,
            notes=f'Burned 0.02858544 ETH in gas from {ADDY}',
            counterparty='gas',
        ), HistoryBaseEntry(
            event_identifier=tx_hash.hex(),  # pylint: disable=no-member
            sequence_index=1,
            timestamp=1598813490000,
            location=Location.BLOCKCHAIN,
            event_type=HistoryEventType.SPEND,
            event_subtype=HistoryEventSubType.RETURN_WRAPPED,
            asset=A_CETH,
            balance=Balance(amount=FVal('24.97649991'), usd_value=ZERO),
            location_label=ADDY,
            notes='Return 24.97649991 cETH to compound',
            counterparty=CPT_COMPOUND,
        ), HistoryBaseEntry(
            event_identifier=tx_hash.hex(),  # pylint: disable=no-member
            sequence_index=2,
            timestamp=1598813490000,
            location=Location.BLOCKCHAIN,
            event_type=HistoryEventType.WITHDRAWAL,
            event_subtype=HistoryEventSubType.REMOVE_ASSET,
            asset=A_ETH,
            balance=Balance(amount=FVal('0.500003923413507454'), usd_value=ZERO),
            location_label=ADDY,
            notes='Withdraw 0.500003923413507454 ETH from compound',
            counterparty=CPT_COMPOUND,
        ), HistoryBaseEntry(
            event_identifier=tx_hash.hex(),  # pylint: disable=no-member
            sequence_index=49,
            timestamp=1598813490000,
            location=Location.BLOCKCHAIN,
            event_type=HistoryEventType.RECEIVE,
            event_subtype=HistoryEventSubType.REWARD,
            asset=A_COMP,
            balance=Balance(amount=FVal('0.000034845643426795')),
            location_label=ADDY,
            notes='Collect 0.000034845643426795 COMP from compound',
            counterparty=CPT_COMPOUND,
        )]
    assert events == expected_events