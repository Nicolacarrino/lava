import typing as ty
import unittest

from lava.magma.compiler.executable import Executable
from lava.magma.core.process.message_interface_enum import ActorType
from lava.magma.core.resources import HeadNode, Loihi2System
from lava.magma.compiler.node import Node, NodeConfig
from lava.magma.runtime.runtime import Runtime


class TestRuntime(unittest.TestCase):
    def test_runtime_creation(self):
        """Tests runtime constructor"""
        exe: Executable = Executable()
        mp = ActorType.MultiProcessing
        runtime: Runtime = Runtime(exe=exe,
                                   message_infrastructure_type=mp)
        expected_type: ty.Type = Runtime
        self.assertIsInstance(
            runtime, expected_type,
            f"Expected type {expected_type} doesn't match {(type(runtime))}")

    def test_executable_node_config_assertion(self):
        """Tests runtime constructions with expected constraints"""
        exec: Executable = Executable()

        runtime1: Runtime = Runtime(exec, ActorType.MultiProcessing)
        with self.assertRaises(IndexError):
            runtime1.initialize()

        node: Node = Node(HeadNode, [])
        exec.node_configs.append(NodeConfig([node]))
        runtime2: Runtime = Runtime(exec, ActorType.MultiProcessing)
        runtime2.initialize()
        expected_type: ty.Type = Runtime
        self.assertIsInstance(
            runtime2, expected_type,
            f"Expected type {expected_type} doesn't match {(type(runtime2))}")
        runtime2.stop()

        exec1: Executable = Executable()
        node1: Node = Node(Loihi2System, [])
        exec1.node_configs.append(NodeConfig([node1]))
        runtime3: Runtime = Runtime(exec1, ActorType.MultiProcessing)
        with self.assertRaises(AssertionError):
            runtime3.initialize(0)

        exec.node_configs.append(NodeConfig([node]))
        runtime4: Runtime = Runtime(exec, ActorType.MultiProcessing)
        runtime4.initialize(0)
        self.assertEqual(len(runtime4._executable.node_configs), 2,
                         "Expected node_configs length to be 2")
        node2: Node = Node(Loihi2System, [])
        exec.node_configs[0].append(node2)
        self.assertEqual(len(runtime4._executable.node_configs[0]), 2,
                         "Expected node_configs[0] node_config length to be 2")
        runtime4.stop()


if __name__ == "__main__":
    unittest.main()
