#!/bin/bash

# Check if running with sh, re-execute with bash
if [ "$(ps -p $$ -ocomm=)" = "sh" ]; then
  echo "Re-running with bash..."
  exec bash "$0" "$@"
fi

# Default values
bind_address="0.0.0.0"
port=8000
key="${PYTHON_SERVER_KEY:-}"

print_usage() {
    echo "Usage: bash start.sh [OPTIONS]"
    echo "Options:"
    echo "  -b BIND_ADDRESS     Set the bind address (default: 0.0.0.0)"
    echo "  -p PORT             Set the port number (default: 8000)"
    echo "  -k KEY              Set the key (default: PYTHON_SERVER_KEY environment variable or 'defaultKey' if not set)"
    echo "  --help, -h          Show this help message"
}

if [ "$1" == "--help" ] || [ "$1" == "-h" ]; then
    print_usage
    exit 0
fi

# Process command line options
while getopts "b:p:k:" opt; do
  case ${opt} in
    b ) # process bind address
      bind_address="$OPTARG"
      ;;
    p ) # process port
      port="$OPTARG"
      ;;
    k ) # process key
      key="$OPTARG"
      ;;
    \? ) echo "Usage: cmd [-b bind_address] [-p port] [-k key]"
      exit 1
      ;;
  esac
done

# Check if bind address was provided, if not, ask the user
if [ "$bind_address" == "0.0.0.0" ]; then
    echo "Please select the bind option:"
    echo "1. Localhost (bind to 127.0.0.1)"
    echo "2. All interfaces (bind to 0.0.0.0)"

    read -p "Enter the number corresponding to your choice: " choice
    if [ "$choice" == "1" ]; then
        bind_address="localhost"
    elif [ "$choice" == "2" ]; then
        bind_address="0.0.0.0"
    else
        echo "Invalid choice. Using 0.0.0.0 as the default."
        bind_address="0.0.0.0"
    fi
fi

# Check if port was provided, if not, ask the user
if [ -z "$port" ]; then
    read -p "Please enter the port number (press Enter for default): " port
    port="${port:-8000}"  # Set default port as 8000 if user presses Enter
fi

# Check if key was provided or already exists in the environment, if not, ask the user
if [ -z "$key" ]; then
    read -p "Please enter the key (press Enter for default): " key
    key="${key:-defaultKey}"  # Set default key as "defaultKey" if user presses Enter
else
    echo "PYTHON_SERVER_KEY already configured."
fi

# Get the PID of the running process on the specified port and terminate it
pid=$(lsof -i :$port | awk 'NR>1 {print $2}')
if [ -n "$pid" ]; then
    echo "Terminating the running process on port $port (PID: $pid)..."
    kill $pid
    wait $pid  # Wait for the process to finish
fi

# Set the PYTHON_SERVER_KEY environment variable if necessary
if [ -z "$PYTHON_SERVER_KEY" ]; then
    export PYTHON_SERVER_KEY="$key"
fi

# Start the Gunicorn server
echo "Starting the Gunicorn server with bind on $bind_address:$port..."
cd ..
gunicorn main:app --bind $bind_address:$port
