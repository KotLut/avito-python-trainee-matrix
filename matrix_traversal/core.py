import asyncio
from typing import List
import aiohttp


class MatrixError(Exception):
    pass


async def get_matrix(url: str) -> List[int]:
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url, timeout=aiohttp.ClientTimeout(total=10)) as response:
                response.raise_for_status()
                text = await response.text()
    except aiohttp.ClientError as e:
        raise MatrixError(f"Сетевая ошибка при получении матрицы: {e}")
    except asyncio.TimeoutError:
        raise MatrixError("Превышено время ожидания ответа от сервера")

    return _parse_and_traverse(text)


def _parse_and_traverse(text: str) -> List[int]:
    # Парсинг: берем только строки с '|', разбиваем, убираем пробелы, конвертируем в int
    rows = []
    for line in text.strip().split('\n'):
        if line.startswith('|'):
            row = [int(x.strip()) for x in line.strip('|').split('|')]
            rows.append(row)

    if not rows:
        raise MatrixError("Не удалось распарсить матрицу: пустой или некорректный формат")

    # Обход против часовой стрелки: Вниз -> Вправо -> Вверх -> Влево
    result = []
    top, bottom = 0, len(rows) - 1
    left, right = 0, len(rows[0]) - 1

    while top <= bottom and left <= right:
        # 1. Вниз слева
        for i in range(top, bottom + 1):
            result.append(rows[i][left])
        left += 1

        # 2. Вправо по низу
        for i in range(left, right + 1):
            result.append(rows[bottom][i])
        bottom -= 1

        # 3. Вверх справа
        if left <= right:
            for i in range(bottom, top - 1, -1):
                result.append(rows[i][right])
            right -= 1

        # 4. Влево по верху
        if top <= bottom:
            for i in range(right, left - 1, -1):
                result.append(rows[top][i])
            top += 1

    return result
