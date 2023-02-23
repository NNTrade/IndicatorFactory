from __future__ import annotations
from ...indicator_settings import IndicatorSettingsBuilder, Dict, IndicatorSettings


class MASettings(IndicatorSettings):
    @staticmethod
    def wrap(indicator_settigns: IndicatorSettings) -> MASettings:
        return MASettings(indicator_settigns.indicator_type, indicator_settigns.parameters)

    def __init__(self, indicator_type: str, parameters: Dict[str, float]) -> None:
        if MASettingsBuilder.PERIOD_PARAMETER_NAME not in parameters.keys():
            raise Exception(
                f"Parameters does not have {MASettingsBuilder.PERIOD_PARAMETER_NAME}")

        super().__init__(indicator_type, parameters)

    @property
    def period(self) -> float:
        return self._parameters[MASettingsBuilder.PARAMETERS_DICT_FIELD]


class MASettingsBuilder(IndicatorSettingsBuilder):
    PERIOD_PARAMETER_NAME = "priod"
    SMA_NAME = "SMA"
    EMA_NAME = "EMA"

    @staticmethod
    def create_sma_setting(period: float) -> MASettings:
        return MASettingsBuilder(MASettingsBuilder.SMA_NAME, period).build()

    @staticmethod
    def create_ema_setting(period: float) -> MASettings:
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

    def build(self) -> MASettings:
        return MASettings(self.indicator_type, self.parameters)
