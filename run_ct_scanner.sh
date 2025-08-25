#!/bin/bash

# ---------------------------
# EC2 Go + Python Pipeline Manager
# ---------------------------

# Paths relative to repo root
OUTPUT_DIR="Output/Gungnir_Reports"
LOG_FILE="log.txt"
GO_DIR="GO Scanner"
GO_INPUT="Output/Full_Cleaned_Report/total_filtered_domains.txt"
PY_SCRIPT="scripts/ct_scanner.py"

# ---------------------------
# Helper functions
# ---------------------------
get_pipeline_pids() {
    ps aux | grep '[c]t_scanner.py\|[g]o run' | awk '{print $2}'
}

start_pipeline() {
    if [ "$(get_pipeline_pids)" ]; then
        echo "[!] Pipeline already running. PID(s): $(get_pipeline_pids)"
        return
    fi

    echo "[*] Ensuring output folder exists..."
    mkdir -p "$OUTPUT_DIR"

    echo "[*] Starting pipeline in background..."
    nohup sh -c "go run '$GO_DIR' -r '$GO_INPUT' | python3 '$PY_SCRIPT'" > "$LOG_FILE" 2>&1 &
    PIPELINE_PID=$!
    echo "[*] Pipeline started with PID $PIPELINE_PID"
    echo "[*] Logs are being written to $LOG_FILE"
}

stop_pipeline() {
    PIDS=$(get_pipeline_pids)
    if [ -z "$PIDS" ]; then
        echo "[!] No running pipeline processes found."
        return
    fi
    echo "[*] Stopping processes: $PIDS"
    kill $PIDS
    echo "[*] Done."
}

check_logs() {
    if [ ! -f "$LOG_FILE" ]; then
        echo "[!] Log file does not exist yet."
        return
    fi
    echo "[*] Tailing log file ($LOG_FILE)..."
    tail -f "$LOG_FILE"
}

# ---------------------------
# Main
# ---------------------------
case "$1" in
    start)
        start_pipeline
        ;;
    stop)
        stop_pipeline
        ;;
    logs)
        check_logs
        ;;
    *)
        echo "Usage: $0 {start|stop|logs}"
        ;;
esac
