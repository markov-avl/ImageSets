import asyncio
import sys
from base64 import b64encode
from aiohttp import ClientSession
from json import dump


async def get_encoded_image(session: ClientSession) -> str:
    async with session.get('https://picsum.photos/750/450') as response:  # качает рандомные изображения 750x450
        return b64encode(await response.content.read()).decode("utf-8")


async def get_image_set(session: ClientSession) -> set[str]:
    return {await get_encoded_image(session) for _ in range(15)}  # количество фотографий в сете


def save_image_set(image_set: set, image_set_number: int) -> None:
    with open(f'image-sets/image-set-{image_set_number}.json', 'w') as outfile:
        dump(list(image_set), outfile, indent=2)


async def perform_the_task(session: ClientSession, task_number: int) -> None:
    save_image_set(await get_image_set(session), task_number)


async def main() -> None:
    async with ClientSession() as session:
        await asyncio.gather(*[perform_the_task(session, i) for i in range(100)])  # количество сетов


if __name__ == '__main__':
    loop = asyncio.new_event_loop()
    loop.run_until_complete(main())
    loop.close()
    sys.exit()
