import pytest
from unittest.mock import AsyncMock, MagicMock
from src.aggregator import RegionAggregator


@pytest.mark.asyncio
async def test_aggregator(mocker) -> None:
    data = {
        "region": "Europe",
        "total_population": 100000,
        "max_country": "Ukraine",
        "max_population": 100000,
        "min_country": "Ukraine",
        "min_population": 100000,
    }

    mock_mappings = MagicMock()
    mock_mappings.all.return_value = [data]

    mock_result = MagicMock()
    mock_result.mappings.return_value = mock_mappings

    mock_session = AsyncMock()
    mock_session.execute.return_value = mock_result

    mock_session_cls = mocker.patch("src.aggregator.AsyncSessionLocal")
    mock_session_cls.return_value.__aenter__.return_value = mock_session

    result = await RegionAggregator.get_region()

    mock_session.execute.assert_awaited_once()

    assert result == [data]
