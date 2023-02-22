from .settings_builder import IndicatorSettings, MASettingsBuilder
from .indicator import sma, ema, AbsIndicator


def get_ma(settings: IndicatorSettings) -> AbsIndicator:
  if settings.indicator_type == MASettingsBuilder.EMA_NAME:
    return ema(settings)
  if settings.indicator_type == MASettingsBuilder.SMA_NAME:
    return sma(settings)
  raise Exception("Wrong indicator type. Expect SMA or EMA")
