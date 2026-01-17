# from langgraph_sdk import get_client
# import asyncio
# # 调用Agent发布的API接口
# client = get_client(url = "http://localhost:2024")
#
# async def main():
#     async for chunk in client.runs.stream(
#         None,
#         "agent",
#         input={
#             "messages":[{
#                 "role": "human",
#                 "content": "给当前用户一个祝福语"
#             }],
#         },
#         config={"configurable": {'username': 'jared'}}
#     ):
#         print(f"Receiving new event of type: {chunk.event}...")
#         print(chunk.data)
#         print("\n\n")
#         if isinstance(chunk.data, list) and 'type' in chunk.data[0] and chunk.data[0]['type'] == 'ai':
#             print(chunk.data[0]['content'], end='|')
#
# if __name__ == "__main__":
#     asyncio.run(main())