import pytest
from unittest.mock import AsyncMock
from src.print_data import main


@pytest.mark.asyncio
async def test_main_correct_data(mocker, capsys) -> None:
    data = [
        {
            "region": "Europe",
            "total_population": 38000000,
            "max_country": "Ukraine",
            "max_population": 38000000,
            "min_country": "Ukraine",
            "min_population": 38000000,
        }
    ]
    mock_get_region = mocker.patch(
        "src.aggregator.RegionAggregator.get_region",
        new_callable=AsyncMock,
        return_value=data,
    )
    await main()

    mock_get_region.assert_awaited_once()
    captured = capsys.readouterr()

    assert "Region: Europe" in captured.out
    assert "Total population: 38000000" in captured.out
    assert "No data in Database" not in captured.out


@pytest.mark.asyncio
async def test_main_incorrect_data(mocker, capsys) -> None:
    mock_get_region = mocker.patch(
        "src.aggregator.RegionAggregator.get_region",
        new_callable=AsyncMock,
        return_value=[],
    )
    await main()

    mock_get_region.assert_awaited_once()
    captured = capsys.readouterr()

    assert "No data in Database" in captured.out
