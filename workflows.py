import random

from dbos import DBOS
from pydantic_ai import Agent
from pydantic_ai.models.fallback import FallbackModel


claude_agent = Agent("anthropic:claude-sonnet-4-6")
openai_agent = Agent("openai:gpt-5.4")
fallback_agent = Agent(FallbackModel("openai:gpt-5.4", "anthropic:claude-sonnet-4-6"))


@DBOS.workflow()
def chat_workflow(id, provider):
    print(f"started chat_workflow {id=}")
    output = output_type()
    response = chat(provider, output)
    result = response.output if response else ""
    print(f"{id=} result: {result}")
    print(f"finished chat_workflow {id=}")
    return result


@DBOS.step()
def output_type():
    return random.choice(["haiku", "limerick", "sonnet", "couplet", "acrostic"])


@DBOS.step()
def chat(provider, output):
    with open("./sotu.txt", "r") as infile:
        content = infile.read()
    print(f"Contents: {len(content):,}")
    prompt = f"Summarize this text with a {output} poem. No commentary, just the poem.\n\nContents:\n{content}"
    print(f"Prompt: {prompt[0:500]}...")
    if provider == "anthropic":
        return claude_agent.run_sync(prompt)
    elif provider == "openai":
        return openai_agent.run_sync(prompt)
    elif provider == "fallback":
        return fallback_agent.run_sync(prompt)
