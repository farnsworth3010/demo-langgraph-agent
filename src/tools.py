"""Tools for interacting with the ticket system via LangChain."""

from typing import Any

from langchain.tools import tool

from models.ticket import Ticket
from service.ticket_service import TicketService

_service = TicketService()


# User tools
@tool
def create_ticket(
    title: str,
    priority: str,
    category: str,
    client_name: str,
    description: str,
    steps_taken: str,
    email: str,
) -> dict[str, Any]:
    """Create a new ticket."""
    payload: dict[str, Any] = {
        "title": title,
        "priority": priority,
        "category": category,
        "client_name": client_name,
        "description": description,
        "steps_taken": steps_taken,
        "email": email,
    }
    return _service.create_ticket(payload)


# Admin tools
@tool
def get_ticket(ticket_id: int) -> Ticket | None:
    """Return a single ticket by id, or None if not found."""
    return _service.get_ticket(ticket_id)


@tool
def list_tickets(limit: int = 100, page: int = 1) -> list[Ticket]:
    """Return up to `limit` tickets, ordered from newest to oldest."""
    return _service.list_tickets(limit, page)


@tool
def delete_ticket(ticket_id: int) -> None:
    """Delete a ticket by id."""
    _service.delete_ticket(ticket_id)
