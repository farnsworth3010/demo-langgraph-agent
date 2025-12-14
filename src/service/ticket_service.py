"""Ticket service: business logic and validation for tickets."""

from __future__ import annotations

from typing import Any

from models.ticket import Ticket
from repository.ticket_repository import TicketRepository


class TicketService:
    """Service layer that validates and manages tickets."""

    def __init__(self, repo: TicketRepository | None = None) -> None:
        """Initialize the service with an optional repository instance."""
        self.repo = repo or TicketRepository()

    def create_ticket(self, payload: dict) -> dict[str, Any]:
        """Validate the payload and create a ticket. Returns the new ticket id.

        Expected keys: title, priority, category, client_name, description, steps_taken, email
        """
        ticket = Ticket(**payload)

        try:
            new_id = self.repo.insert(ticket)
            return {"success": True, "id": new_id}
        except Exception as e:
            return {"success": False, "error": str(e)}

    def get_ticket(self, ticket_id: int) -> Ticket | None:
        """Return the Ticket object by id or None if not found."""
        t = self.repo.get(ticket_id)
        return t

    def list_tickets(self, limit: int = 100, page: int = 1) -> list[Ticket]:
        """Return a list of tickets up to `limit`."""
        return self.repo.list(limit, page)

    def delete_ticket(self, ticket_id: int) -> None:
        """Delete a ticket by id."""
        self.repo.delete(ticket_id)
