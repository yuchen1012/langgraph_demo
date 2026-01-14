from langgraph_sdk import get_sync_client

# 调用Agent发布的API接口
client = get_sync_client(url="http://localhost:2024")

for chunk in client.runs.stream(
    None,
    "agent",
    input={
        "messages": [{
            "role": "human",
            "content": "What's the weather like in New York?"
        }],
    },
        stream_mode="messages"
):
    print(f"Receiving new event of type: {chunk.event}...")
    print(chunk.data)
    print("\n\n")

# if __name__ == "__main__":
#     run(main())
