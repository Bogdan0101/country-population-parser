from sqlalchemy import text
from src.db import AsyncSessionLocal


class RegionAggregator:
    @staticmethod
    async def get_region() -> list[dict]:
        stmt = text("""
            SELECT
                region,
                SUM(population) as total_population,
                (ARRAY_AGG(location ORDER BY population DESC))[1] AS max_country,
                (ARRAY_AGG(population ORDER BY population DESC))[1] AS max_population,
                (ARRAY_AGG(location ORDER BY population ASC))[1] AS min_country,
                (ARRAY_AGG(population ORDER BY population ASC))[1] AS min_population
            FROM countries
            GROUP BY region
            ORDER BY total_population DESC
        """)
        async with AsyncSessionLocal() as session:
            result = await session.execute(stmt)
            return result.mappings().all()
