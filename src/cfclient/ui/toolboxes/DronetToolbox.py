#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#     ||          ____  _ __
#  +------+      / __ )(_) /_______________ _____  ___
#  | 0xBC |     / __  / / __/ ___/ ___/ __ `/_  / / _ \
#  +------+    / /_/ / / /_/ /__/ /  / /_/ / / /_/  __/
#   ||  ||    /_____/_/\__/\___/_/   \__,_/ /___/\___/
#
#  Copyright (C) 2011-2013 Bitcraze AB
#
#  Crazyflie Nano Quadcopter Client
#
#  This program is free software; you can redistribute it and/or
#  modify it under the terms of the GNU General Public License
#  as published by the Free Software Foundation; either version 2
#  of the License, or (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#  You should have received a copy of the GNU General Public License along with
#  this program; if not, write to the Free Software Foundation, Inc.,
#  51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.
"""
A detachable toolbox for showing console printouts from the Crazyflie
"""
from PyQt5 import QtWidgets
from PyQt5 import uic
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtCore import Qt

import cfclient

__author__ = ''
__all__ = ['DronetToolbox']

console_class = uic.loadUiType(
    cfclient.module_path + "/ui/toolboxes/dronetToolbox.ui")[0]


class DronetToolbox(QtWidgets.QWidget, console_class):
    """Dronet toolbox for showing printouts from the Crazyflie"""
    update = pyqtSignal(str)

    def __init__(self, helper, *args):
        super(DronetToolbox, self).__init__(*args)
        self.setupUi(self)

        self.flyButton.clicked.connect(self._toggle_dronet)
        self.helper = helper
        self.is_flying = 0

    def getName(self):
        return 'Dronet'

    def _toggle_dronet(self):
        if self.is_flying:
            self.helper.cf.param.set_value('START_STOP.fly', 0)
        else:
            self.helper.cf.param.set_value('START_STOP.fly', 1)
        print("Toggling dronet")

    def _fly_param_changed(self, name, value):
        self.is_flying = bool(int(value))
        if self.is_flying:
            self.flyButton.setText("Dronet: LAND");
        else:
            self.flyButton.setText("Dronet: FLY");


    def enable(self):
        self.helper.cf.param.add_update_callback(group='START_STOP', name='fly',
                                         cb=self._fly_param_changed)

    def disable(self):
        # self.helper.cf.console.receivedChar.remove_callback(
        #     self._console_updated)
        pass

    def preferedDockArea(self):
        return Qt.BottomDockWidgetArea
