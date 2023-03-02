import unittest
import logging
from src.indicator_settings import IndicatorSettings


class IndicatorSettings_TestCase(unittest.TestCase):

  logger = logging.getLogger(__name__)
  logging.basicConfig(format='%(asctime)s %(module)s %(levelname)s: %(message)s',
                      datefmt='%m/%d/%Y %I:%M:%S %p', level=logging.INFO)

  def test_WHEN_get_hash_THEN_hash_const(self):
    # Array
    ind_s = IndicatorSettings("test", {"V1": 11, "V2": 22})
    expected_hash = 4650750250
    # Act
    asserted_hash = hash(ind_s)

    # Assert
    self.logger.info(f"Asserted hash {asserted_hash}")
    self.assertEqual(asserted_hash, expected_hash,
                     f"Asserted hash != expected hash")
