from dbos import DBOS
from pydantic_ai import Agent

PROMPT = "Be concise, reply with one sentence."

claude_agent = Agent("anthropic:claude-sonnet-4-6", instructions=PROMPT)
openai_agent = Agent("openai:gpt-5.4", instructions=PROMPT)


@DBOS.workflow()
def chat_workflow(id, provider, prompt):
    print(f"started chat_workflow {id=}")
    result = chat(provider, prompt)
    print(f"{id=} {prompt=}, {result=}")
    print(f"finished chat_workflow {id=}")
    return result


@DBOS.step()
def chat(provider, prompt):
    if provider == "anthropic":
        return claude_agent.run_sync(prompt)
    elif provider == "openai":
        return openai_agent.run_sync(prompt)
