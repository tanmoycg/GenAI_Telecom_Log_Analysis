import random
import datetime
import re
import json
import os

SYNTHETIC_LOG_FILE = "5g_logs.txt"
LOG_FILE_DIRECTORY = "generated_logs"
NO_OF_LOGS = 100
CONFIG_FILE_EVENT_TYPES = "config_event_types.txt"
CONFIG_DIRECTORY = "configs"

# Global variable to store differrnt event types
events = []
    
# load event types from config file and update the global variable "events"
def load_event_types(config_dir, event_config_file):
    global events
    with open(os.path.join(config_dir, event_config_file), "r") as f:
        events = f.readlines()
    events = [event.strip() for event in events]
    if __name__ == "__main__":
        print(events)
    """for line in events[:5]:  # Print first 5 event types
        print(line.strip())
    """
    
# Generate(returns) a single random log entry 
def generate_log():
    global events
    network_functions = ["AMF", "SMF", "UPF", "PCF", "UDM", "NSSF", "AUSF"]
    plmns = ["310-170", "311-480", "404-45"]
    apns = ["internet", "ims", "enterprise"]
    qos_levels = ["Low", "Medium", "High"]
    traffic_types = ["VoLTE", "Data", "Streaming"]
    causes = ["Normal Release", "Network Congestion", "UE Power Off"]
    auth_fail_reasons = ["Wrong Credentials", "Network Timeout", "SIM Expired"]
    slices = ["eMBB", "mMTC", "URLLC"]
    responses = ["Success", "Failure"]
    retries = [1, 2, 3]
    latencies = [10, 20, 50, 100]
    durations = [30, 60, 120, 300]
    recovery_actions = ["Restart AMF", "Re-route Traffic", "Alert NOC"]
    actions_taken = ["Rate Limit Applied", "Temporary Block", "Traffic Re-route"]
    cell_ids = [1001, 1002, 1003, 1004]
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    function = random.choice(network_functions)
    imsi = f"31017{random.randint(1000000, 9999999)}"  # Fake IMSI
    ip = f"192.168.{random.randint(0, 255)}.{random.randint(1, 255)}"
    event_template = random.choice(events)
    event = event_template.format(
        imsi=imsi,
        ip=ip,
        plmn=random.choice(plmns),
        apn=random.choice(apns),
        qos=random.choice(qos_levels),
        traffic=random.choice(traffic_types),
        cause=random.choice(causes),
        auth_fail_reason=random.choice(auth_fail_reasons),
        slice=random.choice(slices),
        response=random.choice(responses),
        retries=random.choice(retries),
        timestamp=timestamp,
        latency=random.choice(latencies),
        duration=random.choice(durations),
        amf_id=f"AMF-{random.randint(100, 999)}",
        recovery_action=random.choice(recovery_actions),
        action_taken=random.choice(actions_taken),
        cell_id_src=random.choice(cell_ids),
        cell_id_dest=random.choice(cell_ids)
    )

    return f"[{timestamp}] [{function}] {event}"

# Create synthetic log file having "no_of_logs" log(s)
def create_log_file(log_directory, log_file_name, no_of_logs):
    #create the directory (Don't throw exception if exists)
    os.makedirs(log_directory, exist_ok=True)
    with open(os.path.join(log_directory, log_file_name), "w") as f:
        for _ in range(no_of_logs):  # Generate "num_of_logs" log entries
            f.write(generate_log() + "\n")
    if __name__ == "__main__":
        print(f"Synthetic logs saved as {SYNTHETIC_LOG_FILE}", )

# Read log file and return a list of logs
def read_logs_from_file(log_directory, log_file_name):
    with open(os.path.join(log_directory, log_file_name), "r") as f:
        logs = f.readlines()
    logs = [log.strip() for log in logs]
    if __name__ == "__main__":
        for line in logs[:5]:  # Print first 5 log entries
            print(line.strip())
    return logs

# Parse timestamp, function and message from a single log
def parse_log(log):
    match = re.match(r"\[(.*?)\] \[(.*?)\] (.*)", log)
    if match:
        timestamp, function, message = match.groups()
        return {"timestamp": timestamp, "function": function, "message": message}
    return None
    
# Process (parse) all logs and returns a list of parsed logs
# One parsed log is represented as a dictionary 
def parse_all_logs(list_of_logs):
    parsed_logs = []
    for log in list_of_logs:
        parsed_log = parse_log(log.strip())
        if parsed_log:
            parsed_logs.append(parsed_log)
    
    # Print first 5 structured logs
    if __name__ == "__main__":
        for log in parsed_logs[:5]:
            print(json.dumps(log, indent=4))
        
    return parsed_logs

# Returns paresed logs as "list of dicts" to the caller
def get_parsed_logs():
    load_event_types(CONFIG_DIRECTORY, CONFIG_FILE_EVENT_TYPES)
    create_log_file(LOG_FILE_DIRECTORY, SYNTHETIC_LOG_FILE, NO_OF_LOGS)
    logs = read_logs_from_file(LOG_FILE_DIRECTORY, SYNTHETIC_LOG_FILE)
    parsed_logs = parse_all_logs(logs)
    return parsed_logs

# Returns raw logs as "list" to the caller 
def get_raw_logs():
    load_event_types(CONFIG_DIRECTORY, CONFIG_FILE_EVENT_TYPES)
    create_log_file(LOG_FILE_DIRECTORY, SYNTHETIC_LOG_FILE, NO_OF_LOGS)
    logs = read_logs_from_file(LOG_FILE_DIRECTORY, SYNTHETIC_LOG_FILE)
    return logs

# For testing, if run as a standalone script    
if __name__ == "__main__":
    get_raw_logs()
    #get_parsed_logs()
