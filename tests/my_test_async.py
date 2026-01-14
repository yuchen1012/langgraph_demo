from langgraph_sdk import get_client
import asyncio
# 调用Agent发布的API接口
client = get_client(url = "http://localhost:2024")

async def main():
    async for chunk in client.runs.stream(
        None,
        "agent",
        input={
            "messages":[{
                "role": "human",
                "content": "What's the weather like in New York?"
            }],
        },
    ):
        print(f"Receiving new event of type: {chunk.event}...")
        print(chunk.data)
        print("\n\n")

if __name__ == "__main__":
    asyncio.run(main())