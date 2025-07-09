# main.py (entrypoint)
import asyncio
from team import get_dsa_team
from autogen_agentchat.messages import TextMessage
from autogen_agentchat.base import TaskResult

async def main():
    team = get_dsa_team()
    task = "Write a function to add two numbers."

    async for message in team.run_stream(task=task):
        if isinstance(message, TextMessage):
            print(f"{message.source}: {message.content}")
        elif isinstance(message, TaskResult):
            print("Stop Reason:", message.stop_reason)

if __name__ == "__main__":
    asyncio.run(main())
