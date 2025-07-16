from neo4j import AsyncGraphDatabase, AsyncDriver
from dotenv import load_dotenv
import os

load_dotenv()

NEO4J_URI = os.getenv("NEO4J_URI", "bolt://127.0.0.1:7687")
NEO4J_USER = os.getenv("NEO4J_USER", "neo4j")
NEO4J_PASSWORD = os.getenv("NEO4J_PASSWORD", "Test@1234")

driver: AsyncDriver = None

async def init_neo4j():
    global driver
    try:
        driver = AsyncGraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASSWORD))
        async with driver.session() as session:
            result = await session.run("RETURN 1")
            await result.single()
        print("✅ Connected to Neo4j successfully.")
    except Exception as e:
        print(f"[Neo4j Connection Error]: {e}")
        raise

async def close_neo4j():
    global driver
    if driver:
        await driver.close()
        print("🛑 Neo4j connection closed.")

def get_driver() -> AsyncDriver:
    if not driver:
        raise RuntimeError("Neo4j driver is not initialized.")
    return driver

async def query_neo4j(query: str, parameters: dict = {}):
    async with driver.session() as session:
        result = await session.run(query, parameters)
        records = []
        async for record in result:
            records.append(record.data())
        return records
