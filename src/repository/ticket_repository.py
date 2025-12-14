"""Repository for storing tickets (simple SQL-backed storage)."""

from __future__ import annotations

from db import get_connection
from models.ticket import Ticket


class TicketRepository:
    """Repository responsible for simple database access for tickets."""

    def __init__(self):
        """Create a repository instance and obtain a DB connection."""
        self.conn = get_connection()

    def insert(self, ticket: Ticket) -> int:
        """Insert a ticket into the DB and return the new record id."""
        cur = self.conn.execute(
            """
            INSERT INTO tickets (title, priority, category, client_name, description, steps_taken, email)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            (
                ticket.title,
                ticket.priority,
                ticket.category,
                ticket.client_name,
                ticket.description,
                ticket.steps_taken,
                ticket.email,
            ),
        )
        self.conn.commit()
        last = cur.lastrowid

        return int(last) if last is not None else 0

    def get(self, ticket_id: int) -> Ticket | None:
        """Return a Ticket object by id or None if not found."""
        cur = self.conn.execute("SELECT * FROM tickets WHERE id = ?", (ticket_id,))
        row = cur.fetchone()

        if not row:
            return None

        return Ticket(**dict(row))

    def list(self, limit: int = 100, page: int = 1) -> list[Ticket]:
        """Return up to `limit` tickets ordered from newest to oldest."""
        offset = (page - 1) * limit
        cur = self.conn.execute(
            "SELECT * FROM tickets ORDER BY created_at DESC LIMIT ? OFFSET ?",
            (limit, offset),
        )
        rows = cur.fetchall()

        return [Ticket(**dict(r)) for r in rows]

    def delete(self, ticket_id: int) -> None:
        """Delete a ticket by id."""
        self.conn.execute("DELETE FROM tickets WHERE id = ?", (ticket_id,))
        self.conn.commit()
