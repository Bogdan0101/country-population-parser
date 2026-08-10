import asyncio
from src.db import init_db, save_countries
from src.parser import Parsers


async def main():
    await init_db()
    data = await Parsers.get_parser("wikipedia").scrap()
    print(data)

    if data:
        await save_countries(data)
        print("Save to db is successful")
    else:
        print("Error: Save to db is unsuccessful")


if __name__ == "__main__":
    asyncio.run(main())
