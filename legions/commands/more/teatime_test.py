from legions.commands.more.teatime import SUPPORTED_BY, SUPPORTED_BY_ALL_CLIENTS, scan
from teatime.plugins.context import NodeType


def test_consistency_of_plugin_lists():
    """
    Tests the consistency of the SUPPORTED_BY_ALL_CLIENTS and SUPPORTED_BY
    plugin lists.
    """
    # Tests that each plugin supported by all clients is also supported by each
    # individual client.
    for client in [NodeType.GETH, NodeType.PARITY]:
        got = all(plugin in SUPPORTED_BY[client] for plugin in SUPPORTED_BY_ALL_CLIENTS)
        assert got == True

    # Tests that the intersection of the plugins supported only by individual
    # clients is the set of plugins supported by all clients.
    plugins_geth = set(SUPPORTED_BY[NodeType.GETH])
    plugins_parity = set(SUPPORTED_BY[NodeType.PARITY])
    plugins_all = set(SUPPORTED_BY_ALL_CLIENTS)

    assert plugins_geth.intersection(plugins_parity) == plugins_all
    assert plugins_parity.intersection(plugins_geth) == plugins_all


def test_plugin_instantiator():
    """
    Tests that each plugin is contained in the scan.pluginInstantiator dict.
    """
    instantiator_plugins = scan.pluginInstantiator.keys()

    # Tests the SUPPORTED_BY lists.
    for client in [NodeType.GETH, NodeType.PARITY]:
        got = all(plugin in instantiator_plugins for plugin in SUPPORTED_BY[client])
        assert got == True

    # Tests the SUPPORTED_BY_ALL_CLIENTS list.
    got = all(plugin in instantiator_plugins for plugin in SUPPORTED_BY_ALL_CLIENTS)
    assert got == True
