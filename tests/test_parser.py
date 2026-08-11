import pytest
from unittest.mock import AsyncMock, MagicMock
from src.parser import WikipediaParser, Parsers


@pytest.mark.asyncio
async def test_wikipedia_scrap(mocker) -> None:
    fake_html = "<html>fake</html>"
    data = [{"location": "Ukraine", "population": 38000000, "region": "Europe"}]

    mock_response = MagicMock()
    mock_response.text = fake_html

    mock_client = AsyncMock()
    mock_client.get.return_value = mock_response

    mock_async_client_cls = mocker.patch("src.parser.httpx.AsyncClient")
    mock_async_client_cls.return_value.__aenter__.return_value = mock_client

    parser = WikipediaParser()
    mocker.patch.object(
        parser,
        "parse",
        return_value=data,
    )
    result = await parser.scrap()
    mock_client.get.assert_awaited_once_with(parser.url, headers=parser.headers)
    assert result == data


def test_wikipedia_parse() -> None:
    fake_html = """
        <div id="mwLw">
            <table>
                <tr>
                    <td><a rel="mw:WikiLink" title="Ukraine">Ukraine</a></td>
                    <td>extra</td>
                    <td>38,000,000</td>
                    <td>extra</td>
                    <td><a rel="mw:WikiLink" title="Europe">Europe</a></td>
                    <td>extra</td>
                </tr>
            </table>
        </div>
        """
    parser = WikipediaParser()
    result = parser.parse(fake_html)

    assert len(result) == 1
    assert result[0] == {
        "location": "Ukraine",
        "population": 38000000,
        "region": "Europe",
    }


def test_wikipedia_parse_no_body() -> None:
    fake_html = "<div>No target table here</div>"
    parser = WikipediaParser()
    result = parser.parse(fake_html)

    assert result == []


def test_get_parser_success() -> None:
    parser = Parsers.get_parser("Wikipedia")
    assert isinstance(parser, WikipediaParser)


def test_get_parser_unknown() -> None:
    name_parser = "unknown"
    with pytest.raises(ValueError, match=f"Parser {name_parser} does not exist."):
        Parsers.get_parser(name_parser)
