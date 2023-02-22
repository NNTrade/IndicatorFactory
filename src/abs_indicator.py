from abc import ABC
import pandas as pd
from .progress_log import ProgressLog
from .indicator_settings import IndicatorSettings
from logging import getLogger


class AbsIndicator(ABC):
  """Abstract calculator of indicator
  """
  IS_LAST_COL_NAME = "isLast"

  def __init__(self, settings: IndicatorSettings) -> None:
    self._settings = settings
    self._logger = getLogger(f"IndicatorBuilder[{settings.indicator_type}]")
    super().__init__()

  @property
  def settings(self) -> IndicatorSettings:
    return self._settings

  def loopByQuoteDataFrame(self, work_df: pd.DataFrame, index_len_log: int = 6):
    if AbsIndicator.IS_LAST_COL_NAME not in work_df.columns:
      work_df[AbsIndicator.IS_LAST_COL_NAME] = 1

    progressLog = ProgressLog(index_len_log, logger=self._logger)

    for index, row in work_df.iterrows():
      self._next(index, row, bool(row[AbsIndicator.IS_LAST_COL_NAME]))

      progressLog.check(index)

    self.finish()

  def _next(self, index: int, row: pd.Series, is_last: bool):
    ...

  def finish(self):
    ...

  @property
  def result(self) -> pd.DataFrame:
    ...
