#!/usr/bin/env python3
# -*- encoding: utf-8; py-indent-offset: 4 -*-
# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
#
# This file is part of the check_mk bird check.
#
# The check_mk bird check is free software: you can redistribute it
# and/or modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation, either version 3 of
# the License, or (at your option) any later version.
#
# The check_mk bird check is distributed in the hope that it will
# be useful, but WITHOUT ANY WARRANTY; without even the implied
# warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
# See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with it. If not, see <http://www.gnu.org/licenses/>.
#
# Copyright 2014 by Frederik Kriewitz <frederik@kriewitz.eu>.

from cmk.graphing.v1 import perfometers

def _perfometer_bird_protocols(name: str) -> perfometers.Perfometer:
    return perfometers.Perfometer(
        name=name,
        focus_range=perfometers.FocusRange(
            lower=perfometers.Closed(0),
            upper=perfometers.Open(40000),
        ),
        segments=["route_stats_imported"],
    )

perfometer_bird_protocols = _perfometer_bird_protocols("bird_protocols")
perfometer_bird6_protocols = _perfometer_bird_protocols("bird6_protocols")

def _perfometer_bird_memory(name: str) -> perfometers.Perfometer:
    return perfometers.Perfometer(
        name=name,
        focus_range=perfometers.FocusRange(
            lower=perfometers.Closed(0),
            upper=perfometers.Open(900),
        ),
        segments=["Total"],
    )

perfometer_bird_memory = _perfometer_bird_memory("bird_memory")
perfometer_bird6_memory = _perfometer_bird_memory("bird6_memory")
