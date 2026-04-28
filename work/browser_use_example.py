import asyncio
from browser_use import Agent, Browser
from langchain_ollama import ChatOllama


async def main():
    browser = Browser()

    llm = ChatOllama(
        model="qwen3.6:latest",
        base_url="http://pythagoras.csis.oita-u.ac.jp:11434",
    )

    agent = Agent(
#        task="食べログで「大分駅 ラーメン」を検索してお店の情報やレビューを収集し、ファイルに出力する",
        task="Googleで大分大学を検索して公式サイトのタイトルを取得する",
        llm=llm,
        browser=browser,
        enable_memory=False,
    )
    await agent.run()


if __name__ == "__main__":
    asyncio.run(main())
