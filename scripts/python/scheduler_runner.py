import os
import subprocess
import datetime
import logging
import sys
import time
from datetime import datetime


# PROJECT PATHS

 
BASE_DIR = os.path.dirname(
    os.path.dirname(
        os.path.dirname(
            os.path.abspath(__file__)
        )
    )
)

output_dir = os.path.join(BASE_DIR, "outputs")


# OUTPUT DIRECTORY


os.makedirs(output_dir, exist_ok=True)


# OUTPUT FILE


script_name = os.path.splitext(
    os.path.basename(__file__)
)[0]

output_file = os.path.join(
    output_dir,
    f"{script_name}_output.txt"
)


# TEE OUTPUT CLASS


class Tee:

    def __init__(self, *files):
        self.files = files

    def write(self, obj):
        for file in self.files:
            file.write(obj)
            file.flush()

    def flush(self):
        for file in self.files:
            file.flush()



# OUTPUT STREAM


output_stream = open(
    output_file,
    "w",
    encoding="utf-8"
)


# DUPLICATE OUTPUT


sys.stdout = Tee(sys.stdout, output_stream)

sys.stderr = Tee(sys.stderr, output_stream)



# START EXECUTION TIMER


execution_start = datetime.now()
script_start_time = time.time()

print(
    f"Execution Started At: "
    f"{execution_start.strftime('%Y-%m-%d %H:%M:%S')}"
)

print("=" * 50)


# LOGS DIRECTORY


logs_dir = os.path.join(BASE_DIR, "logs")

os.makedirs(logs_dir, exist_ok=True)


# OUTPUTS DIRECTORY


outputs_dir = os.path.join(BASE_DIR, "outputs")

os.makedirs(outputs_dir, exist_ok=True)


# LOG FILE


log_file = os.path.join(
    logs_dir,
    "scheduler.log"
)

logging.basicConfig(
    filename=log_file,
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)


# STATUS FILE


status_file = os.path.join(
    outputs_dir,
    "scheduler_status.txt"
)


# CURRENT TIME


current_time = datetime.now()



# EXECUTE SCHEDULED TASK


try:

    logging.info(
        "Scheduler task started"
    )

    task_start_time =  datetime.now()

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

    task_end_time =  datetime.now()

    execution_time = task_end_time - task_start_time

    
    # WRITE STATUS FILE
    

    with open(status_file, "w") as file:

        file.write(
            "AZURE TASK SCHEDULER STATUS\n"
        )

        file.write(
            "...............\n\n"
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
            "Next Run : Tomorrow 22:00 \n"
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
            "...............\n\n"
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


# EXECUTION TIME


script_end_time = time.time()

execution_time = round(
    script_end_time - script_start_time,
    2
)

execution_end = datetime.now()

print("\n" + "=" * 50)

print(
    f"Execution Completed At: "
    f"{execution_end.strftime('%Y-%m-%d %H:%M:%S')}"
)

print(
    f"Execution Time: "
    f"{execution_time} seconds"
)

print("=" * 50)

# output_stream.close()