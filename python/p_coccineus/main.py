import json
import os
from typing import Literal, TypedDict

import bpy

Unit = Literal["NONE", "METRIC", "IMPERIAL"]
RotationUnit = Literal["DEGREES", "RADIANS"]
LengthUnit = Literal[
    "ADAPTIVE",
    "KILOMETERS",
    "METERS",
    "CENTIMETERS",
    "MILLIMETERS",
    "MICROMETERS"
]
MassUnit = Literal[
    "ADAPTIVE",
    "TONNES",
    "KILOGRAMS",
    "GRAMS",
    "MILLIGRAMS"
]
TimeUnit = Literal[
    "ADAPTIVE",
    "DAYS",
    "HOURS",
    "MINUTES",
    "SECONDS",
    "MILLISECONDS",
    "MICROSECONDS"
]
TemperatureUnit = Literal[
    "ADAPTIVE",
    "KELVIN",
    "CELSIUS"
]


class SceneUnitSetting(TypedDict):
    unit_system: Unit
    unit_scale_length: float
    use_separate_units: bool
    rotation_unit: RotationUnit
    length_unit: LengthUnit
    mass_unit: MassUnit
    time_unit: TimeUnit
    temperature_unit: TemperatureUnit


class SceneUnitSettingValidationResult(TypedDict):
    unit_system: tuple[bool, Unit, Unit]
    unit_scale_length: tuple[bool, float, float]
    use_separate_units: tuple[bool, bool, bool]
    rotation_unit: tuple[bool, RotationUnit, RotationUnit]
    length_unit: tuple[bool, LengthUnit, LengthUnit]
    mass_unit: tuple[bool, MassUnit, MassUnit]
    time_unit: tuple[bool, TimeUnit, TimeUnit]
    temperature_unit: tuple[bool, TemperatureUnit, TemperatureUnit]


def this_dir() -> str:
    return os.path.normpath(os.path.abspath(os.path.dirname(__file__)))


def validate_scene_unit(actual_setting: SceneUnitSetting) -> SceneUnitSettingValidationResult:
    _setting = bpy.data.scenes["Scene"].unit_settings

    scene_unit_setting = {
        "unit_system": _setting.system,
        "unit_scale_length": _setting.scale_length,
        "use_separate_units": _setting.use_separate,
        "rotation_unit": _setting.system_rotation,
        "length_unit": _setting.length_unit,
        "mass_unit": _setting.mass_unit,
        "time_unit": _setting.time_unit,
        "temperature_unit": _setting.temperature_unit
    }

    return {
        _key: (
            scene_unit_setting[_key] == _actual,
            scene_unit_setting[_key],
            _actual
        )
        for _key, _actual in actual_setting.items()
    }


def validate_scene_setting():
    unit_setting_file_path = os.path.join(this_dir(), "config", "actual_unit_setting.json")
    with open(unit_setting_file_path, "r", encoding="utf-8-sig") as fp:
        _setting = json.load(fp)

    _result = validate_scene_unit(_setting)

    print("##### Validation result #####")
    print("===== Unit setting =====")
    for _unit, (_ok, _scene, _actual) in _result.items():
        ok = "OK" if _ok else "NG"
        print(f"{_unit}\n{ok}\nscene: {_scene}\nactual: {_actual}\n")
