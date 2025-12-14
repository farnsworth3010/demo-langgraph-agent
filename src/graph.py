"""Definition of agents for ticket support and administration."""

from langchain.agents import create_agent
from langchain.chat_models import init_chat_model

from db import init_db
from prompts.admin import ADMIN_SYSTEM_PROMPT as ADMIN_PROMPT
from prompts.support import SUPPORT_SYSTEM_PROMPT as SUPPORT_PROMPT
from tools import (
    create_ticket,
    delete_ticket,
    get_ticket,
    list_tickets,
)

init_db()

llm = init_chat_model(
    model="qwen/qwen3-4b",
    base_url="http://localhost:1234/v1",
    model_provider="openai",
    temperature=0.7,
    api_key="not_needed",
)

support = create_agent(
    model=llm,
    tools=[
        create_ticket,
    ],
    system_prompt=SUPPORT_PROMPT,
)

admin = create_agent(
    model=llm,
    tools=[
        get_ticket,
        list_tickets,
        delete_ticket,
    ],
    system_prompt=ADMIN_PROMPT,
)
