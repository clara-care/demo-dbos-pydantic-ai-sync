import datetime
import itertools
import sys
import time

from dbos import DBOSClient

from worker import DBOS_SYSTEM_DATABASE_URL, queue

WORKFLOW_NAME = "chat_workflow"

PROMPTS = [
    "How many 'r's are there in Daryl Strawberry's Strawberry Ranch?",
    "How much wood could a wood chuck chuck if a wood chuck could chuck wood. Answer seriously without commentary in stones.",
    "Where am I? Here. What time is it? Now.",
    "Rank the top 15 US President by beard length in their official portrait (longest to shortest). Make your best guess with no added commentary.",
    "List every US state capital that contains the letter 'x'. Return only the list, no commentary.",
    "What is the largest prime number smaller than 1000? Answer with just the number.",
    "Name the only country in the world whose name contains all five vowels. No explanation.",
    "How many sides does a rhombicosidodecahedron have? Answer with a single number.",
    "Translate 'I would like a glass of water' into Latin, Ancient Greek, and Esperanto. One line each.",
    "What year did the last country in the world abolish chattel slavery (not counting serfdom)? Just the year.",
    "List the seven deadly sins in alphabetical order. No preamble.",
    "What is the most southerly capital city in the world? Answer in one word.",
    "If you wrote out every integer from 1 to 100, how many times does the digit 7 appear? Just a number.",
    "Name a mammal that lays eggs. One word answer only.",
]


def main():
    provider = sys.argv[1].strip().lower() if len(sys.argv) > 1 else None
    if provider not in ("openai", "anthropic"):
        raise ValueError(
            f"Provider must be one of 'openai' or 'anthropic', got: {provider=}"
        )

    handles = enqueue_work(provider, PROMPTS)
    wait_for_workflows(handles)


def enqueue_work(provider, prompts):
    client = DBOSClient(system_database_url=DBOS_SYSTEM_DATABASE_URL)
    handles = []
    for index, prompt in enumerate(prompts):
        handle = client.enqueue(
            {
                "queue_name": queue.name,
                "workflow_name": WORKFLOW_NAME,
            },
            index,
            provider,
            prompt,
        )
        handles.append(handle)

    return handles


def wait_for_workflows(handles):
    deadline = datetime.datetime.now() + datetime.timedelta(minutes=5)
    while datetime.datetime.now() < deadline:
        statuses = [h.get_status() for h in handles]
        if all(is_workflow_done(s) for s in statuses):
            break

        print(summarize(statuses))

        time.sleep(1)


def is_workflow_done(workflow_status):
    return workflow_status.status not in ("ENQUEUED", "DELAYED", "PENDING")


def get_status(workflow_status):
    return workflow_status.status


def summarize(statuses):
    summary = itertools.groupby(sorted(statuses, key=get_status), key=get_status)
    return ", ".join(
        f"{status}: {len(list(workflows)):,}" for status, workflows in summary
    )


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        pass

    print("Done")
