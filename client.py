import datetime
import itertools
import sys
import time

from dbos import DBOSClient

from worker import DBOS_SYSTEM_DATABASE_URL, queue


def main():
    provider = sys.argv[1].lower()
    if provider not in ("openai", "anthropic", "fallback"):
        raise ValueError(
            f"Provider must be one of 'openai' or 'anthropic', got: {provider=}"
        )
    try:
        count = int(sys.argv[2]) if len(sys.argv) > 2 else 10
    except ValueError:
        raise ValueError("Invalid count")

    handles = enqueue_work(provider, count)
    wait_for_workflows(handles)
    for i, handle in enumerate(handles):
        print(f"Result #{i}:\n{handle.get_result()}\n\n")


def enqueue_work(provider, count):
    client = DBOSClient(system_database_url=DBOS_SYSTEM_DATABASE_URL)
    handles = []
    for index in range(count):
        handle = client.enqueue(
            {
                "queue_name": queue.name,
                "workflow_name": "chat_workflow",
            },
            index,
            provider,
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
