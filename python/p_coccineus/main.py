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

FileFormat = Literal[
    "BMP",
    "IRIS",
    "PNG",
    "JPEG",
    "JPEG2000",
    "TARGA",
    "TARGA_RAW",
    "CINEON",
    "DPX",
    "OPEN_EXR_MULTILAYER",
    "OPEN_EXR",
    "HDR",
    "TIFF",
    "WEBP",
    "AVI_JPEG",
    "AVI_RAW",
    "FFMPEG",
]

FFmpegEncoding = Literal[
    "MPEG1",
    "MPEG2",
    "MPEG4",
    "AVI",
    "QUICKTIME",
    "DV",
    "OGG",
    "MKV",
    "FLASH",
    "WEBM",
]
FFmpegVideoCodec = Literal[
    "NONE",
    "DNXHD",
    "DV",
    "FFV1",
    "FLASH",
    "H264",
    "HUFFYUV",
    "MPEG1",
    "MPEG2",
    "MPEG4",
    "PNG",
    "QTRLE",
    "THEORA",
    "WEBM",
    "AV1",
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


class RenderSetting(TypedDict):
    frame_start: int
    frame_end: int
    frame_step: int
    output_dir: str
    file_format: FileFormat


class RenderSettingValidationResult(TypedDict):
    frame_start: tuple[bool, int, int]
    frame_end: tuple[bool, int, int]
    frame_step: tuple[bool, int, int]
    output_dir: tuple[bool, str, str]
    file_format: tuple[bool, FileFormat, FileFormat]


def this_dir() -> str:
    return os.path.normpath(os.path.abspath(os.path.dirname(__file__)))


def validate_scene_unit_setting(actual_setting: SceneUnitSetting) -> SceneUnitSettingValidationResult:
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


def validate_render_setting(actual_setting: RenderSetting) -> RenderSettingValidationResult:
    _setting = bpy.data.scenes["Scene"]

    render_setting = {
        "frame_start": _setting.frame_start,
        "frame_end": _setting.frame_end,
        "frame_step": _setting.frame_step,
        "output_dir": _setting.render.filepath,
        "file_format": _setting.render.image_settings.file_format,
    }

    return {
        _key: (
            render_setting[_key] == _actual,
            render_setting[_key],
            _actual
        )
        for _key, _actual in actual_setting.items()
    }


def validate_scene_setting():
    unit_setting_file_path = os.path.join(this_dir(), "config", "actual_unit_setting.json")
    with open(unit_setting_file_path, "r", encoding="utf-8-sig") as fp:
        _setting = json.load(fp)

    print("##### Validation result #####")

    _result_scene_unit = validate_scene_unit_setting(_setting["scene_unit"])
    print("===== Scene unit setting =====")
    for _unit, (_ok, _scene, _actual) in _result_scene_unit.items():
        ok = "OK" if _ok else "NG"
        print(f"{_unit}\n{ok}\nscene: {_scene}\nactual: {_actual}\n")

    print("")

    _result_render = validate_render_setting(_setting["render"])
    print("===== Render setting =====")
    for _unit, (_ok, _scene, _actual) in _result_render.items():
        ok = "OK" if _ok else "NG"
        print(f"{_unit}\n{ok}\nscene: {_scene}\nactual: {_actual}\n")
