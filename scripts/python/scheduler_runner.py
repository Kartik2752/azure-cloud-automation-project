import os
import subprocess
import datetime
import logging

# ==========================================
# PROJECT PATHS
# ==========================================

BASE_DIR = os.path.dirname(
    os.path.dirname(
        os.path.dirname(
            os.path.abspath(__file__)
        )
    )
)

# ==========================================
# LOGS DIRECTORY
# ==========================================

logs_dir = os.path.join(BASE_DIR, "logs")

os.makedirs(logs_dir, exist_ok=True)

# ==========================================
# OUTPUTS DIRECTORY
# ==========================================

outputs_dir = os.path.join(BASE_DIR, "outputs")

os.makedirs(outputs_dir, exist_ok=True)

# ==========================================
# LOG FILE
# ==========================================

log_file = os.path.join(
    logs_dir,
    "scheduler.log"
)

logging.basicConfig(
    filename=log_file,
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)

# ==========================================
# STATUS FILE
# ==========================================

status_file = os.path.join(
    outputs_dir,
    "scheduler_status.txt"
)

# ==========================================
# CURRENT TIME
# ==========================================

current_time = datetime.datetime.now()

# ==========================================
# EXECUTE SCHEDULED TASK
# ==========================================

try:

    logging.info(
        "Scheduler task started"
    )

    start_time = datetime.datetime.now()

    result = subprocess.run(
        [
            "python",

            os.path.join(
                BASE_DIR,
                "scripts",
                "python",
                "stop_vm.py"
            )
        ],
        capture_output=True,
        text=True
    )

    end_time = datetime.datetime.now()

    execution_time = end_time - start_time

    # ==========================================
    # WRITE STATUS FILE
    # ==========================================

    with open(status_file, "w") as file:

        file.write(
            "AZURE TASK SCHEDULER STATUS\n"
        )

        file.write(
            "=============================\n\n"
        )

        file.write(
            f"Last Run Time : "
            f"{current_time}\n"
        )

        file.write(
            "Task Status : SUCCESS\n"
        )

        file.write(
            f"Execution Time : "
            f"{execution_time}\n"
        )

        file.write(
            "Next Run : Tomorrow 10:00 PM\n"
        )

    logging.info(
        "Scheduler task completed successfully"
    )

    logging.info(
        f"Execution Time: {execution_time}"
    )

    logging.info(
        f"Script Output: {result.stdout}"
    )

    print(
        "Scheduler Automation Completed"
    )

except Exception as e:

    logging.error(
        f"Scheduler failed: {e}"
    )

    with open(status_file, "w") as file:

        file.write(
            "AZURE TASK SCHEDULER STATUS\n"
        )

        file.write(
            "=============================\n\n"
        )

        file.write(
            f"Last Run Time : "
            f"{current_time}\n"
        )

        file.write(
            "Task Status : FAILED\n"
        )

        file.write(
            f"Error : {e}\n"
        )

    print(f"Error: {e}")