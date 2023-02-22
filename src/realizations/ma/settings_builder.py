from __future__ import annotations
from ...indicator_settings import IndicatorSettingsBuilder, Dict, IndicatorSettings


class MASettingsBuilder(IndicatorSettingsBuilder):
  PERIOD_PARAMETER_NAME = "priod"
  SMA_NAME = "SMA"
  EMA_NAME = "EMA"

  @staticmethod
  def create_sma_setting(period: float) -> IndicatorSettings:
    return MASettingsBuilder(MASettingsBuilder.SMA_NAME, period).build()

  @staticmethod
  def create_ema_setting(period: float) -> IndicatorSettings:
    return MASettingsBuilder(MASettingsBuilder.EMA_NAME, period).build()

  def __init__(self, indicator_type: str, period: float) -> None:
    if indicator_type not in [MASettingsBuilder.SMA_NAME, MASettingsBuilder.EMA_NAME]:
      raise Exception("Wrong indicator type")

    super().__init__(indicator_type, {
        MASettingsBuilder.PERIOD_PARAMETER_NAME: period})

  @property
  def period(self) -> float:
    return self.parameters[MASettingsBuilder.PERIOD_PARAMETER_NAME]

  @period.setter
  def period(self, new_period: float):
    self.parameters[MASettingsBuilder.PERIOD_PARAMETER_NAME] = new_period

  def set_period(self, new_period: float) -> MASettingsBuilder:
    self.period = new_period
    return self
