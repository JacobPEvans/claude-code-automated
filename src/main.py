import asyncio
import logging

from src.cli import create_parser
from src.commands.execute import execute_command
from src.commands.plan import plan_command
from src.commands.update import update_command

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")


async def main():
    parser = create_parser()
    args = parser.parse_args()

    if args.command == "plan":
        plan_command(args)
    elif args.command == "execute":
        await execute_command(args)
    elif args.command == "update":
        update_command(args)


if __name__ == "__main__":
    asyncio.run(main())
