from __future__ import annotations
from typing import Dict

class IndicatorSettings:
  TYPE_DICT_FIELD = "type"
  PARAMETERS_DICT_FIELD = "parameters"

  def __init__(self, indicator_type: str, parameters: Dict[str, float]) -> None:
    self._indicator_type = indicator_type
    self._parameters = parameters.copy()
    self.__hash = hash(self._indicator_type) * hash(frozenset(self.parameters.items()))
    pass

  @property
  def indicator_type(self) -> str:
    return self._indicator_type

  @property
  def parameters(self) -> Dict[str, float]:
    return self._parameters.copy()

  def __hash__(self):
    return self.__hash

  def __eq__(self, other: IndicatorSettings):
    if self.__class__ != other.__class__:
      return False
    return self.indicator_type == other.indicator_type and self.parameters == other.parameters

  @staticmethod
  def from_dict(config: Dict[str, any]) -> IndicatorSettings:
    return IndicatorSettings(config[IndicatorSettings.TYPE_DICT_FIELD], config[IndicatorSettings.PARAMETERS_DICT_FIELD])

  def to_dict(self) -> Dict[str, any]:
    return {
        IndicatorSettings.TYPE_DICT_FIELD: self._indicator_type,
        IndicatorSettings.PARAMETERS_DICT_FIELD: self.parameters
    }

  def copy(self)->IndicatorSettings:
    return IndicatorSettings(self._indicator_type, self._parameters.copy())

class IndicatorSettingsBuilder(IndicatorSettings):

    def __init__(self, indicator_type: str = None,
                 args: Dict[str, float] = {}) -> None:
        super().__init__(indicator_type, args.copy())

    @property
    def indicator_type(self) -> str:
        return super().indicator_type

    @indicator_type.setter
    def indicator_type(self, new_value: str) -> float:
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
