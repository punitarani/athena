"""athena/openalex/download.py"""


import re
from pathlib import Path

import fitz
import httpx

from athena.utils import get_logger, sanitize_name, save_sanitized_name

from ..config import PAPERS_DIR
from .models import WorkObject

# Ensure the directories exist
PAPERS_PDF_DIR = PAPERS_DIR.joinpath("pdf")
PAPERS_PDF_DIR.mkdir(parents=True, exist_ok=True)

logger = get_logger(__name__)


async def get_paper_text(work: WorkObject) -> str:
    """
    Get the text of the paper.
    If not downloaded, download it first.

    Args:
        work (WorkObject): Work object

    Returns:
        str: Extracted text from the paper

    TODO: read the txt file instead of the pdf file
    """
    doi = str(work.doi)

    # Handle the case where the DOI is not found
    if doi is None:
        logger.error(f"No DOI found for work: {work.title}")
        return ""

    # Remove the prefix "https://doi.org/" from the DOI
    if doi.startswith("https://doi.org/"):
        doi = doi[16:]
    elif doi.startswith("http://doi.org/"):
        doi = doi[15:]
    elif doi.startswith("doi.org/"):
        doi = doi[8:]

    filename = sanitize_name(doi)
    filepath = PAPERS_PDF_DIR.joinpath(filename + ".pdf")

    # If the file already exists, extract the text and return it
    if filepath.exists():
        return extract_text(filepath)

    # Download the paper
    downloaded_path = await download_paper(work)

    if downloaded_path is None:
        logger.error(f"Failed to download paper: {doi}")
        return ""

    # Extract the text from the downloaded paper
    return extract_text(downloaded_path)


async def download_paper(work: WorkObject) -> Path | None:
    """
    Download the paper from the Unpaywall API.

    Args:
        work (Work): Work object

    Returns:
        Path | None: Path to the downloaded paper or None if not found
    """
    doi = str(work.doi)

    # Handle the case where the DOI is not found
    if doi is None:
        return None

    # Remove the prefix "https://doi.org/" from the DOI
    if doi.startswith("https://doi.org/"):
        doi = doi[16:]
    elif doi.startswith("http://doi.org/"):
        doi = doi[15:]
    elif doi.startswith("doi.org/"):
        doi = doi[8:]

    filename = sanitize_name(doi)
    filepath = PAPERS_PDF_DIR.joinpath(filename + ".pdf")

    # If the file already exists, return it
    if filepath.exists():
        logger.info(f"Paper already downloaded: {doi}")
        return filepath

    # Save the sanitized name
    save_sanitized_name(text=doi, name=filename)

    url = None
    if work.best_oa_location:
        url = work.best_oa_location.pdf_url
    if url is None:
        logger.info(f"No PDF URL for work: {doi}")
        return None
    url = str(url)

    try:
        return await download_pdf(doi, url, filepath)
    except Exception as e:
        logger.error(f"Error downloading paper: {doi}: {e}")
        return None


async def download_pdf(doi: str, url: str, filepath: Path) -> Path | None:
    """
    Download the PDF of the paper from the Unpaywall API.

    Args:
        doi (str): DOI of the paper
        url (str): URL of the PDF
        filepath (Path): Path to save the PDF

    Returns:
        str | None: Path to the downloaded PDF or None if not found
    """

    timeout = httpx.Timeout(timeout=60.0, connect=60.0)

    for i in range(3):
        try:
            async with httpx.AsyncClient(timeout=timeout) as client:
                response = await client.get(url, follow_redirects=True)
                content_type = response.headers.get("Content-Type", "")

                # Check MIME type and PDF signature
                if content_type == "application/pdf" or response.content.startswith(
                    b"%PDF-"
                ):
                    with open(filepath, "wb") as f:
                        f.write(response.content)
                    return filepath
                else:
                    logger.debug(
                        f"Attempt {i + 1}: Content is not a PDF. MIME type: {content_type}"
                    )

        except httpx.RequestError as e:
            logger.debug(
                f"Attempt {i + 1}: An error occurred while requesting {url}: {e}"
            )
    logger.error(f"Error downloading paper: {doi}")

    return None


def extract_text(fp: Path) -> str:
    """
    Extract text from a PDF file.

    Args:
        fp (Path): Path to the PDF file

    Returns:
        str: Extracted text from the PDF file
    """

    text = ""
    try:
        with fitz.open(fp) as doc:
            for page in doc:
                page_text = page.get_text()
                text += clean_text(page_text) + " "  # Add a space between pages' text
    except Exception as e:
        logger.error(f"Failed to extract text from {fp}: {e}")
        return ""

    return text.strip()


def clean_text(text: str) -> str:
    """
    Basic text cleaning to remove excessive whitespace.

    Args:
        text (str): Text to clean

    Returns:
        str: Cleaned text
    """
    return re.sub("\s+", " ", text).strip()
