import asyncio
from fastmcp import Client

SERVER_PATH = "src/rag_mcp/server.py"


async def main():
    async with Client(SERVER_PATH) as client:
        tools = await client.list_tools()
        print("Connected. Available tools:", [t.name for t in tools])
        print("Type a question, or 'quit' to exit.\n")

        while True:
            question = input("You: ").strip()
            if question.lower() in ("quit", "exit"):
                break

            result = await client.call_tool("rag_query", {"question": question})
            data = result.data  # structured dict from rag_query's return value
            print(f"\nAnswer: {data['answer']}")
            print("Sources:", [s["source"] for s in data["sources"]])
            print()


if __name__ == "__main__":
    asyncio.run(main())
