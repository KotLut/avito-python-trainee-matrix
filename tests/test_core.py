import pytest
import aiohttp
import asyncio
from unittest.mock import AsyncMock, MagicMock, patch
from matrix_traversal.core import get_matrix, MatrixError

EXPECTED_TRAVERSAL = [
    10, 50, 90, 130,
    140, 150, 160, 120,
    80, 40, 30, 20,
    60, 100, 110, 70,
]

MATRIX_TEXT = """+-----+-----+-----+-----+
|  10 |  20 |  30 |  40 |
+-----+-----+-----+-----+
|  50 |  60 |  70 |  80 |
+-----+-----+-----+-----+
|  90 | 100 | 110 | 120 |
+-----+-----+-----+-----+
| 130 | 140 | 150 | 160 |
+-----+-----+-----+-----+"""


@pytest.mark.asyncio
async def test_get_matrix_success():
    url = "https://fake-url.com/matrix.txt"

    mock_response = MagicMock()
    mock_response.text = AsyncMock(return_value=MATRIX_TEXT)
    mock_response.raise_for_status = MagicMock()

    mock_get_cm = AsyncMock()
    mock_get_cm.__aenter__.return_value = mock_response
    mock_get_cm.__aexit__.return_value = None

    mock_session = MagicMock()
    mock_session.get.return_value = mock_get_cm

    mock_session_cm = AsyncMock()
    mock_session_cm.__aenter__.return_value = mock_session
    mock_session_cm.__aexit__.return_value = None

    with patch('aiohttp.ClientSession', return_value=mock_session_cm):
        result = await get_matrix(url)
        assert result == EXPECTED_TRAVERSAL


@pytest.mark.asyncio
async def test_get_matrix_network_error():
    url = "https://fake-url.com/matrix.txt"

    mock_session = MagicMock()
    mock_session.get.side_effect = aiohttp.ClientError("Connection Refused")

    mock_session_cm = AsyncMock()
    mock_session_cm.__aenter__.return_value = mock_session
    mock_session_cm.__aexit__.return_value = None

    with patch('aiohttp.ClientSession', return_value=mock_session_cm):
        with pytest.raises(MatrixError):
            await get_matrix(url)