"""athena/openalex/search.py"""

import urllib.parse

import httpx


async def search_works(query: str, n: int = 10) -> list:
    """Search for works."""
    base_url = "https://api.openalex.org/works"

    # URL-encode the query string
    query = urllib.parse.quote(query)

    # Construct the URL
    url = f"{base_url}?search={query}"

    # Limit the number of results
    if n is not None:
        url += f"&q={n}"

    # Make the request
    async with httpx.AsyncClient() as client:
        print(f"GET {url}")
        response = await client.get(url)

    # Return the list of works
    return response.json().get("results", [])
