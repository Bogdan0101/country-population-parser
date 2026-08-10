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
        print(f'Top country: {row["max_country"]}')
        print(f'Top country population: {row["max_population"]}')
        print(f'Small country: {row["min_country"]}')
        print(f'Small country population: {row["min_population"]}')
        print("------------------------------")


if __name__ == "__main__":
    asyncio.run(main())
