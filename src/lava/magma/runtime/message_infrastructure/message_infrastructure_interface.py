# Copyright (C) 2021 Intel Corporation
# SPDX-License-Identifier: BSD-3-Clause
# See: https://spdx.org/licenses/
import typing as ty
if ty.TYPE_CHECKING:
    from lava.magma.core.process.process import AbstractProcess
    from lava.magma.compiler.builders.builder import (
        AbstractRuntimeServiceBuilder,
        PyProcessBuilder
    )
from abc import ABC, abstractmethod

from lava.magma.compiler.channels.interfaces import ChannelType, Channel
from lava.magma.core.sync.domain import SyncDomain

"""A Message Infrastructure Interface which can create actors which would
participate in message passing/exchange, start and stop them as well as
declare the underlying Channel Infrastructure Class to be used for message
passing implementation."""


class MessageInfrastructureInterface(ABC):
    """Interface to provide the ability to create actors which can
    communicate via message passing"""
    @abstractmethod
    def start(self):
        """Starts the messaging infrastructure"""
        pass

    @abstractmethod
    def stop(self):
        """Stops the messaging infrastructure"""
        pass

    @abstractmethod
    def build_actor(self, target_fn: ty.Callable, builder: ty.Union[
        ty.Dict['AbstractProcess', 'PyProcessBuilder'], ty.Dict[
            SyncDomain, 'AbstractRuntimeServiceBuilder']]):
        """Given a target_fn starts a system process"""
        pass

    @property
    @abstractmethod
    def actors(self) -> ty.List[ty.Any]:
        """Returns a list of actors"""
        pass

    @abstractmethod
    def channel_class(self, channel_type: ChannelType) -> ty.Type[Channel]:
        """Given the Channel Type, Return the Channel Implementation to
        be used during execution"""
        pass
