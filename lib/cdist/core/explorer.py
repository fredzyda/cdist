# -*- coding: utf-8 -*-
#
# 2011 Steven Armstrong (steven-cdist at armstrong.cc)
# 2011 Nico Schottelius (nico-cdist at schottelius.org)
#
# This file is part of cdist.
#
# cdist is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# cdist is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with cdist. If not, see <http://www.gnu.org/licenses/>.
#
#

import logging
import os

import cdist

log = logging.getLogger(__name__)


'''
common:
    runs only remotely, needs local and remote to construct paths

    env:
        __explorer: full qualified path to other global explorers on remote side
            -> remote.global_explorer_path

a global explorer is:
    - a script
    - executed on the remote side
    - returns its output as a string

    env:

    creates: nothing, returns output

type explorer is:
    - a script
    - executed on the remote side for each object instance
    - returns its output as a string

    env:
        __object: full qualified path to the object's remote dir
        __object_id: the objects id
        __object_fq: full qualified object id, iow: $type.name + / + object_id
        __type_explorer: full qualified path to the other type explorers on remote side

    creates: nothing, returns output

'''


class Explorer(object):
    """Executes cdist explorers.

    """
    def __init__(self, target_host, local, remote):
        self.target_host = target_host
        self.local = local
        self.remote = remote
        self.env = {
            '__target_host': self.target_host,
            '__explorer': self.remote.global_explorer_path,
        }

    ### global

    def list_global_explorer_names(self):
        """Return a list of global explorer names."""
        return os.listdir(self.local.global_explorer_path)

    def transfer_global_explorers(self):
        """Transfer the global explorers to the remote side."""
        self.remote.mkdir(self.remote.global_explorer_path)
        self.remote.transfer(self.local.global_explorer_path, self.remote.global_explorer_path)

    def run_global_explorer(self, explorer):
        """Run the given global explorer and return it's output."""
        script = os.path.join(self.remote.global_explorer_path, explorer)
        return self.remote.run_script(script, env=self.env)

    ### type

    def list_type_explorer_names(self, cdist_type):
        """Return a list of explorer names for the given type."""
        source = os.path.join(self.local.type_path, cdist_type.explorer_path)
        return os.listdir(source)

    def transfer_type_explorers(self, cdist_type):
        """Transfer the type explorers for the given type to the remote side."""
        source = os.path.join(self.local.type_path, cdist_type.explorer_path)
        destination = os.path.join(self.remote.type_path, cdist_type.explorer_path)
        self.remote.mkdir(destination)
        self.remote.transfer(source, destination)

    def transfer_object_parameters(self, cdist_object):
        """Transfer the parameters for the given object to the remote side."""
        source = os.path.join(self.local.object_path, cdist_object.parameter_path)
        destination = os.path.join(self.remote.object_path, cdist_object.parameter_path)
        self.remote.mkdir(destination)
        self.remote.transfer(source, destination)

    def run_type_explorer(self, explorer, cdist_object):
        """Run the given type explorer for the given object and return it's output."""
        cdist_type = cdist_object.type
        env = self.env.copy()
        env.update({
            '__object': cdist_object.absolute_path,
            '__object_id': cdist_object.object_id,
            '__object_fq': cdist_object.path,
            '__type_explorer': os.path.join(self.remote.type_path, cdist_type.explorer_path)
        })
        script = os.path.join(self.remote.type_path, cdist_type.explorer_path, explorer)
        return self.remote.run_script(script, env=env)