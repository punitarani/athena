"""athena/openalex/errors.py"""


class OpenAlexError(ValueError):
    """OpenAlex error"""


class InvalidEntityID(OpenAlexError):
    """Invalid OpenAlex entity ID"""

    def __init__(self, entity_id: str):
        self.entity_id = entity_id
        super().__init__(f"Invalid OpenAlex Entity ID: {entity_id}")
