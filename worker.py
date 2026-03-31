import threading
import uuid

from dbos import DBOS, DBOSConfig, Queue


DBOS_SYSTEM_DATABASE_URL = "sqlite:///demo_dbos_pydantic_ai_sync.sqlite"
DBOS_WORKFLOW_QUEUE_NAME = "workflow-queue"
DBOS_APPLICATION_NAME = "demo-dbos-pydantic-ai-sync"

DBOS_CONFIG: DBOSConfig = {
    "name": DBOS_APPLICATION_NAME,
    "executor_id": str(uuid.uuid4()),
}

queue = Queue("workflow-queue")


if __name__ == "__main__":
    print("Starting up...")

    import workflows  # noqa

    DBOS(config=DBOS_CONFIG)
    DBOS.launch()

    print("Finished start up")
    try:
        threading.Event().wait()
    except KeyboardInterrupt:
        pass
    finally:
        print("Shutting down...")
        DBOS.destroy()

    print("Done")
