import pytest
from unittest.mock import AsyncMock, patch
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
    mock_response = AsyncMock()
    mock_response.text = AsyncMock(return_value=MATRIX_TEXT)
    mock_response.raise_for_status = AsyncMock()
    
    mock_session = AsyncMock()
    mock_session.get.return_value.__aenter__.return_value = mock_response
    
    with patch('aiohttp.ClientSession', return_value=mock_session):
        result = await get_matrix("https://fake-url.com/matrix.txt")
        assert result == EXPECTED_TRAVERSAL

@pytest.mark.asyncio
async def test_get_matrix_network_error():
    mock_session = AsyncMock()
    mock_session.get.side_effect = Exception("Connection Refused")
    
    with patch('aiohttp.ClientSession', return_value=mock_session):
        with pytest.raises(MatrixError):
            await get_matrix("https://fake-url.com/matrix.txt")
