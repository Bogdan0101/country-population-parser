import pytest
from unittest.mock import AsyncMock
from src.get_data import main


@pytest.mark.asyncio
async def test_main_data_correct(mocker, capsys) -> None:
    data_test = [
        {"location": "Ukraine", "population": 38000000, "region": "Europe"},
    ]
    mocker.patch("src.get_data.init_db", new_callable=AsyncMock)
    mock_save_countries = mocker.patch(
        "src.get_data.save_countries", new_callable=AsyncMock
    )

    mock_parser_instance = mocker.MagicMock()
    mock_parser_instance.scrap = AsyncMock(return_value=data_test)
    mocker.patch("src.get_data.Parsers.get_parser", return_value=mock_parser_instance)

    await main()

    mock_save_countries.assert_awaited_once_with(data_test)
    captured = capsys.readouterr()
    assert "Save to db is successful" in captured.out


@pytest.mark.asyncio
async def test_main_data_incorrect(mocker, capsys) -> None:
    mocker.patch("src.get_data.init_db", new_callable=AsyncMock)
    mock_save_countries = mocker.patch(
        "src.get_data.save_countries", new_callable=AsyncMock
    )

    mock_parser_instance = mocker.MagicMock()
    mock_parser_instance.scrap = AsyncMock(return_value=[])
    mocker.patch("src.get_data.Parsers.get_parser", return_value=mock_parser_instance)

    await main()

    mock_save_countries.assert_not_called()
    captured = capsys.readouterr()
    assert "Error: Save to db is unsuccessful" in captured.out
