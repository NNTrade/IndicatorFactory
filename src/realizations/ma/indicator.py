from .columns import MA_COL_NAME
import pandas as pd
from NNTrade.common import CLOSE
from ...abs_indicator import AbsIndicator
from .settings_builder import MASettingsBuilder, IndicatorSettings
import numpy as np
"""_summary_
a = (2 / (period + 1))
EMAt = a * Valuet + (1 - a ) * EMAt-1
или
EMAt = (2 / (period + 1)) * Valuet + ( 1 - (2 / (period + 1)) * EMAt-1
Первое значение принимаем как
EMA1 = Value
"""


class ema(AbsIndicator):
  def __init__(self, settings: IndicatorSettings) -> None:
    self.__period = settings.parameters[MASettingsBuilder.PERIOD_PARAMETER_NAME]
    self.__a = (2 / (self.__period + 1))
    self.clear()
    super().__init__(settings)

  def clear(self):
    self.__ma_data = {}
    self.__ma_sr = None
    self.__prev_ma = None

  @property
  def period(self) -> int:
    return self.__period

  def next(self, index: int, row: pd.Series, is_last: bool):
    cur_close = row[CLOSE]

    if self.__prev_ma is None:
      cur_ma = cur_close
    else:
      cur_ma = self.__a * cur_close + (1 - self.__a) * self.__prev_ma

    self.__ma_data[index] = cur_ma

    if is_last:
      self.__prev_ma = cur_ma

  def finish(self):
    self.__ma_sr = pd.Series(self.__ma_data, name=MA_COL_NAME)

  @property
  def result(self) -> pd.DataFrame:
    return pd.DataFrame(self.__ma_sr)


class sma(AbsIndicator):
  def __init__(self, settings: IndicatorSettings) -> None:
    self.__period = settings.parameters[MASettingsBuilder.PERIOD_PARAMETER_NAME]
    # self.__shift = -(self.__period - 1)
    self.last_values = []
    self.clear()
    super().__init__(settings)

  def clear(self):
    self.__sma_data = {}
    self.__sma_sr = None

  @property
  def period(self) -> int:
    return self.__period

  def next(self, index: int, row: pd.Series, is_last: bool):
    cur_close = row[CLOSE]
    cur_len = len(self.last_values) + 1
    if cur_len > 1:
      self.__sma_data[index] = (np.sum(self.last_values) + cur_close)/cur_len
    else:
      self.__sma_data[index] = cur_close

    if is_last:
      if cur_len == self.period:
        self.last_values.pop(0)
      self.last_values.append(cur_close)

  def finish(self):
    self.__sma_sr = pd.Series(self.__sma_data, name=MA_COL_NAME)

  @property
  def result(self) -> pd.DataFrame:
    return pd.DataFrame(self.__sma_sr)
