from utils.neo4j_db import get_driver

async def get_user(username: str, password: str):
    query = """
    MATCH (u:User {username: $username, password: $password})
    RETURN u.userId AS userId, u.username AS username, u.full_name AS full_name
    """
    driver = get_driver()
    async with driver.session() as session:
        result = await session.run(query, username=username, password=password)
        record = await result.single()
        if record:
            return {
                "userId": record["userId"],
                "username": record["username"],
                "full_name": record["full_name"]
            }
        return None
