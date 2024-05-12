"""athena/openalex/utils.py"""

import requests
from pydantic import HttpUrl

from .errors import OpenAlexError


def parse_id_from_url(url: str | HttpUrl) -> str:
    """
    Parse the ID from an OpenAlex URL
    Parses Work, Author, Institution, and Source IDs.

    Args:
        url (str | HttpUrl): OpenAlex URL

    Returns:
        str: OpenAlex ID
    """
    url = str(url)
    if url.startswith("https://openalex.org/"):
        url = url[21:]
        if url[0] in ["W", "A", "I", "S"]:
            return url
    raise OpenAlexError("Invalid OpenAlex URL")


def doi_to_entity_id(doi: str) -> str:
    """
    Convert a DOI to an OpenAlex entity ID

    Args:
        doi (str): DOI to convert to an OpenAlex entity ID

    Returns:
        str: OpenAlex entity ID
    """

    if not doi.startswith("https://doi.org/"):
        doi = f"https://doi.org/{doi}"

    url = f"https://api.openalex.org/works/doi/{doi}"
    response = requests.get(url)
    response.raise_for_status()

    # Check if the request was successful
    if response.status_code == 200:
        data = response.json()
        return parse_id_from_url(data["id"])
    else:
        raise OpenAlexError(f"Invalid DOI: {doi}")
