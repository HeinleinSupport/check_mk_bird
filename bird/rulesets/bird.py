#!/usr/bin/env python3
# -*- encoding: utf-8; py-indent-offset: 4 -*-
# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4

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

from cmk.rulesets.v1 import (
    Help,
    Title,
)
from cmk.rulesets.v1.form_specs import (
    DataSize,
    DefaultValue,
    DictElement,
    Dictionary,
    IECMagnitude,
    Integer,
    InputHint,
    LevelDirection,
    migrate_to_integer_simple_levels,
    Percentage,
    SimpleLevels,
)
from cmk.rulesets.v1.rule_specs import (
    CheckParameters,
    HostAndItemCondition,
    HostCondition,
    Topic,
)


#   .--Parameter-----------------------------------------------------------.
#   |          ____                                _                       |
#   |         |  _ \ __ _ _ __ __ _ _ __ ___   ___| |_ ___ _ __            |
#   |         | |_) / _` | '__/ _` | '_ ` _ \ / _ \ __/ _ \ '__|           |
#   |         |  __/ (_| | | | (_| | | | | | |  __/ ||  __/ |              |
#   |         |_|   \__,_|_|  \__,_|_| |_| |_|\___|\__\___|_|              |
#   |                                                                      |
#   +----------------------------------------------------------------------+
#   |                                                                      |
#   '----------------------------------------------------------------------'
#.

# bird.status
def _parameter_valuespec_bird_status():
    return Dictionary(
        elements = {
            'uptime_low_threshold': DictElement(
                parameter_form=Integer(
                    title=Title("Warning if uptime is lower than"),
                    unit_symbol="seconds",
                    prefill=DefaultValue(300),
                )),
            'config_file_min_age': DictElement(
                parameter_form=Integer(
                    title=Title("Minimum config file age for last reconfiguration warnings:"),
                    unit_symbol="seconds",
                    prefill=DefaultValue(60),
                )),
        },
        ignored_elements = ("config_files", "memory", "protocols", "status", "version"),
    )

rule_spec_bird_status = CheckParameters(
    name="bird_status",
    topic=Topic.APPLICATIONS,
    parameter_form=_parameter_valuespec_bird_status,
    title=Title("BIRD Status"),
    condition=HostCondition(),
)


# bird.memory
def _parameter_valuespec_bird_memory():
    return Dictionary(
        elements = {
            "memory_levels_Total": DictElement(
                parameter_form=SimpleLevels(
                    title=Title("Total memory usage"),
                    migrate=migrate_to_integer_simple_levels,
                    form_spec_template=DataSize(
                        displayed_magnitudes=[IECMagnitude.GIBI, IECMagnitude.MEBI, IECMagnitude.KIBI],
                    ),
                    level_direction=LevelDirection.UPPER,
                    prefill_fixed_levels=InputHint(value=(0, 0)),
                )),
        },
        ignored_elements = ("config_files", "memory", "protocols", "status", "version"),
    )

# register memory parameters for each BIRD version
rule_spec_bird_memory = CheckParameters(
    name="bird_memory",
    topic=Topic.APPLICATIONS,
    parameter_form=_parameter_valuespec_bird_memory,
    title=Title("BIRD Memory"),
    condition=HostCondition(),
)

rule_spec_bird6_memory = CheckParameters(
    name="bird6_memory",
    topic=Topic.APPLICATIONS,
    parameter_form=_parameter_valuespec_bird_memory,
    title=Title("BIRD6 Memory"),
    condition=HostCondition(),
)

# bird.protocols
def _bird_stats_level(title):
    return Dictionary(
        title=Title(title),
        elements={
            "lower": DictElement(
                parameter_form=SimpleLevels(
                    title=Title("Lower levels"),
                    migrate=migrate_to_integer_simple_levels,
                    help_text=Help(f"Lower levels for the {title} routes"),
                    form_spec_template=Integer(),
                    level_direction=LevelDirection.LOWER,
                    prefill_fixed_levels=InputHint(value=(0, 0)),
                )),
            "upper": DictElement(
                parameter_form=SimpleLevels(
                    title=Title("Upper levels"),
                    migrate=migrate_to_integer_simple_levels,
                    help_text=Help(f"Upper levels for the {title} routes"),
                    form_spec_template=Integer(),
                    level_direction=LevelDirection.UPPER,
                    prefill_fixed_levels=InputHint(value=(0, 0)),
                )),
        }
    )

def _parameter_valuespec_bird_protocols():
    _bird_stats_elements = {}
    for i in ["imported", "filtered", "exported", "preferred"]:
        _bird_stats_elements[i] = DictElement(
            parameter_form=_bird_stats_level(i),
        )
    return Dictionary(
        elements = {
            "route_stats_levels": DictElement(
                parameter_form=Dictionary(
                    title = Title("Route Statistics Levels"),
                    elements = _bird_stats_elements,
                )),
            "route_stats_levels_limit_warning_factor": DictElement(
                parameter_form=Percentage(
                    title=Title("Warning level for limit based thresholds"),
                    prefill=DefaultValue(value=90.0),
                )),
        },
        ignored_elements = ('config_files', 'memory', 'protocols', 'status', 'version'),
    )

# register protocols parameters for each BIRD version
rule_spec_bird_protocols = CheckParameters(
    name="bird_protocols",
    topic=Topic.APPLICATIONS,
    parameter_form=_parameter_valuespec_bird_protocols,
    title=Title("BIRD Protocols"),
    condition=HostAndItemCondition(
        item_title=Title("Protocol"),
    ),
)

rule_spec_bird6_protocols = CheckParameters(
    name="bird6_protocols",
    topic=Topic.APPLICATIONS,
    parameter_form=_parameter_valuespec_bird_protocols,
    title=Title("BIRD6 Protocols"),
    condition=HostAndItemCondition(
        item_title=Title("Protocol"),
    ),
)
