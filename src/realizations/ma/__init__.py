from .builder import get_ma
from .settings_builder import MASettingsBuilder
from ...indicator_factory import IndicatorFactory
from .columns import MA_COL_NAME

IndicatorFactory.register_indicator_global("EMA", get_ma)
IndicatorFactory.register_indicator_global("SMA", get_ma)
