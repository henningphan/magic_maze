import pytest
from magicmaze import Solution
from unittest.mock import MagicMock

@pytest.fixture
def solution():
    mock_api = MagicMock()
    sol = Solution(mock_api)
    return sol
