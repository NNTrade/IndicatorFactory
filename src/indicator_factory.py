from typing import Dict, Callable, List
from .indicator_settings import IndicatorSettings
from .abs_indicator import AbsIndicator
from logging import getLogger


class IndicatorFactory:
  global_registered_indicators: Dict[str, List[Callable[[
      IndicatorSettings], AbsIndicator]]] = {}

  @staticmethod
  def register_indicator_global(indicator_type: str, builder: Callable[[IndicatorSettings], AbsIndicator]):
    builders_list = IndicatorFactory.global_registered_indicators.pop(
        indicator_type, [])

    if len(builders_list) > 0:
      getLogger("IndicatorFactory").warning(
          "Indicator with same name %s is already registered. Remove duplication before using Indicator Factory", indicator_type)
    builders_list.append(builder)

    IndicatorFactory.global_registered_indicators[indicator_type] = builders_list

  def __init__(self) -> None:
    self._registered_indicators: Dict[str, Callable[[
        IndicatorSettings], AbsIndicator]] = {}
    self._logger = getLogger("IndicatorFactory")
    pass

  def register_indicator(self, indicator_type: str, builder: Callable[[IndicatorSettings], AbsIndicator]):
    if indicator_type in self._registered_indicators:
      raise Exception("Indicator with same name is already registered")
    self._registered_indicators[indicator_type] = builder

  def create(self, indicator_settings: IndicatorSettings, priority_to_local: bool = True) -> AbsIndicator:
    local_builer: Callable[[IndicatorSettings], AbsIndicator] = None
    if indicator_settings.indicator_type in self._registered_indicators:
      local_builer = self._registered_indicators[indicator_settings]

    if local_builer is None or not priority_to_local:
      finded_builders: List[Callable[[IndicatorSettings], AbsIndicator]] = []

      if local_builer is not None:
        finded_builders.append(local_builer)

      if indicator_settings.indicator_type in IndicatorFactory.global_registered_indicators:
        finded_builders.extend(IndicatorFactory.global_registered_indicators[
            indicator_settings.indicator_type])

      if len(finded_builders) > 1:
        self._logger.error("Found %i builders for indicator %s: local builder %i, global builders %i", len(
            finded_builders), indicator_settings.indicator_type, int(local_builer is not None), len(finded_builders) - 1)
        raise Exception(
            f"Found several builders for indicator {indicator_settings.indicator_type}")

      if len(finded_builders) <= 0:
        self._logger.error("No builders found for %s indicator",
                           indicator_settings.indicator_type)
        raise Exception(
            f"No builders found for indicator {indicator_settings.indicator_type}")

      return finded_builders[0](indicator_settings)

    return local_builer(indicator_settings)
