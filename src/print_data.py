import asyncio
from src.aggregator import RegionAggregator


async def main():
    data = await RegionAggregator.get_region()

    if not data:
        print("No data in Database")
        return
    for row in data:
        print("------------------------------")
        print(f'Region: {row["region"]}')
        print(f'Total population: {row["total_population"]}')
        print(f'T: {row["max_country"]}')
        print(f'P: {row["max_population"]}')
        print(f'A: {row["min_country"]}')
        print(f'C: {row["min_population"]}')
        print("------------------------------")


if __name__ == "__main__":
    asyncio.run(main())
