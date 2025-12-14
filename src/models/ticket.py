"""Data model for a support ticket."""

from pydantic import BaseModel, Field


class Ticket(BaseModel):
    """Data model for a support ticket."""

    title: str = Field(description="Ticket title")
    priority: str = Field(description="Ticket priority")
    category: str = Field(description="Ticket category")
    client_name: str = Field(description="Client's name")
    description: str = Field(description="Problem description")
    steps_taken: str = Field(description="Steps taken to try to resolve the issue")
    email: str = Field(description="Client's email")
