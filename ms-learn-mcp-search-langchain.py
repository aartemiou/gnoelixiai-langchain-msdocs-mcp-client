"""
Demo Script: Using LangChain with Microsoft Learn Docs MCP Server

This example demonstrates how to use LangChain's MCP client adapter to connect
to the Microsoft Learn Docs MCP server, discover tools, and invoke the 
'microsoft_docs_search' tool to query Microsoft Docs in real time.

Author: Artemakis Artemiou
https://www.linkedin.com/in/aartemiou/
License: MIT
"""
import asyncio
import json
from langchain_mcp_adapters.client import MultiServerMCPClient

async def run_ms_learn_mcp_demo():

    # 1. Initialize the MCP Client
    client = MultiServerMCPClient(
        {
            "mslearn": {
                "transport": "streamable_http",
                "url": "https://learn.microsoft.com/api/mcp",
            }
        }
    )

    # 2. Get the tools from the connected MCP server
    try:
        tools = await client.get_tools() # 
        print("Successfully connected to MS Learn MCP and retrieved tools.")
        for tool in tools:
            print(f"- Tool Name: {tool.name}, Description: {tool.description}")

    except Exception as e:
        print(f"Error connecting to MCP or retrieving tools: {e}")
        print("Please ensure the MCP server is accessible and you have the necessary permissions/headers.")
        return

    # 3. Find the specific Microsoft Docs Search tool
    ms_docs_search_tool = None
    for tool in tools:
        if tool.name == "microsoft_docs_search": 
            ms_docs_search_tool = tool
            break

    if not ms_docs_search_tool:
        print("The 'microsoft_docs_search' tool was not found on the MCP server.")
        return

    print(f"\nFound the tool: {ms_docs_search_tool.name}")

    # 4. Call the microsoft_docs_search tool directly    
    query = input("\nEnter your Microsoft Docs search query: ").strip()

    print(f"\nCalling '{ms_docs_search_tool.name}' with query: '{query}'")

    try:
        payload = {"question": query}
        result = await ms_docs_search_tool.ainvoke(payload)

        print("\n--- Search Results from Microsoft Learn ---")

        parsed_result = json.loads(result)

        for i, item in enumerate(parsed_result, start=1):
            print(f"\nResult {i}: {item['title']}")
            print(f"URL: {item['contentUrl']}")
            print(f"Excerpt:\n{item['content'][:500]}...\n")  # First 500 characters

    except Exception as e:
        print(f"Error calling the tool: {e}")

# Run the program (async function)
if __name__ == "__main__":
    asyncio.run(run_ms_learn_mcp_demo())
