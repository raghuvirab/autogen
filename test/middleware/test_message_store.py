from typing import Dict, Optional, Union

import pytest
from autogen.agentchat.agent import Agent
from autogen.middleware.message_store import MessageStoreMiddleware


def _dummy_reply(
    message: Union[Dict, str],
    sender: Agent,
    request_reply: Optional[bool] = None,
    silent: Optional[bool] = False,
) -> str:
    """Generate a dummy reply."""
    if isinstance(message, str):
        return "Hello World"
    else:
        return {"content": "Hello World", "role": "assistant"}


def test_message_store() -> None:
    md = MessageStoreMiddleware(name="Assistant")
    message = {"role": "user", "content": "Hi there"}
    sender = Agent("User")
    reply = md.call(
        message=message,
        sender=sender,
        request_reply=True,
        silent=False,
        next=_dummy_reply,
    )
    assert reply == {"content": "Hello World", "role": "assistant"}
    assert md.oai_messages[sender] == [
        {"content": "Hi there", "role": "user"},
        {"content": "Hello World", "role": "assistant"},
    ]


@pytest.mark.asyncio()
async def test_message_store_async() -> None:
    md = MessageStoreMiddleware(name="Assistant")
    message = {"role": "user", "content": "Hi there"}
    sender = Agent("User")
    reply = await md.a_call(
        message=message,
        sender=sender,
        request_reply=True,
        silent=False,
        next=_dummy_reply,
    )
    assert reply == {"content": "Hello World", "role": "assistant"}
    assert md.oai_messages[sender] == [
        {"content": "Hi there", "role": "user"},
        {"content": "Hello World", "role": "assistant"},
    ]
