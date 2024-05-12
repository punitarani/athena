"""athena/llm/models.py"""

from pydantic import BaseModel, ValidationError, field_validator


class DocumentMetadata(BaseModel):
    """Metadata for a document"""

    index: int
    work_id: str
    doi: str
    text: str


class Document(BaseModel):
    """Embedding document"""

    id: str
    values: list[float]
    metadata: DocumentMetadata

    @field_validator("id")  # noqa
    @classmethod
    def id_must_contain_hash(cls, v):
        """Validate the id"""
        if "#" not in v:
            raise ValidationError("Document.id must contain '#'")
        return v
