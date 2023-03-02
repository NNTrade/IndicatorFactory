from __future__ import annotations
from abc import ABC
from typing import Dict
from .const_hash import const_hash_arr

def _isinstance(other) -> bool:
    return isinstance(other, __baseSettings)

class __baseSettings(ABC):
    def __init__(self, indicator_type: str, parameters: Dict[str, float]) -> None:
        self._indicator_type = indicator_type
        self._parameters = parameters.copy()

    def to_dict(self) -> Dict[str, any]:
        return {
            IndicatorSettings.TYPE_DICT_FIELD: self._indicator_type,
            IndicatorSettings.PARAMETERS_DICT_FIELD: self._parameters.copy()
        }

    def __str__(self) -> str:
        return str(self.to_dict())

    def __eq__(self, other: __baseSettings):
        return _isinstance(other) and \
            self._indicator_type == other._indicator_type and self._parameters == other._parameters

class IndicatorSettings(__baseSettings):
    TYPE_DICT_FIELD = "type"
    PARAMETERS_DICT_FIELD = "parameters"

    def __init__(self, indicator_type: str, parameters: Dict[str, float]) -> None:
        super().__init__(indicator_type, parameters)
        self.__hash = const_hash_arr(
            [self._indicator_type, *[k+str(v) for k, v in self.parameters.items()]])
        pass

    @property
    def indicator_type(self) -> str:
        return self._indicator_type

    @property
    def parameters(self) -> Dict[str, float]:
        return self._parameters.copy()

    def __hash__(self):
        return self.__hash

    @staticmethod
    def from_dict(config: Dict[str, any]) -> IndicatorSettings:
        return IndicatorSettings(config[IndicatorSettings.TYPE_DICT_FIELD], config[IndicatorSettings.PARAMETERS_DICT_FIELD])


class IndicatorSettingsBuilder(__baseSettings):

    @staticmethod
    def from_dict(config: Dict[str, any]) -> IndicatorSettingsBuilder:
        return IndicatorSettingsBuilder(config[IndicatorSettings.TYPE_DICT_FIELD], config[IndicatorSettings.PARAMETERS_DICT_FIELD])

    def __init__(self, indicator_type: str = None,
                 parameters: Dict[str, float] = {}) -> None:
        super().__init__(indicator_type, parameters)

    @property
    def indicator_type(self) -> str:
        return self._indicator_type

    @indicator_type.setter
    def indicator_type(self, new_value: str):
        self._type = new_value

    def set_indicator_type(self, new_indictor_type: str) -> IndicatorSettingsBuilder:
        self.indicator_type = new_indictor_type
        return self

    @property
    def parameters(self) -> Dict[str, float]:
        return self._parameters

    @parameters.setter
    def parameters(self,  parameters_dict: Dict[str, float]):
        self._parameters = parameters_dict

    def set_parameters(self, parameters_dict: Dict[str, float]) -> IndicatorSettingsBuilder:
        self.parameters = parameters_dict
        return self

    def set_parameter(self, key: str, value:  float) -> IndicatorSettingsBuilder:
        self._parameters[key] = value
        return self

    def build(self) -> IndicatorSettings:
        return IndicatorSettings(self.indicator_type, self.parameters)

    def copy(self) -> IndicatorSettingsBuilder:
        return IndicatorSettingsBuilder(self._indicator_type, self._parameters.copy())
