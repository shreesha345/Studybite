import subprocess
import os
import sys
import argparse

def run_command(command, cwd=None):
    """
    Execute a shell command and handle its output
    """
    try:
        process = subprocess.run(
            command,
            cwd=cwd,
            shell=True,
            check=True,
            text=True,
            capture_output=True
        )
        print(f"Success: {command}")
        print(process.stdout)
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error executing {command}")
        print(f"Error message: {e.stderr}")
        return False

def get_frontend_container_id():
    """
    Get the container ID of the frontend container
    """
    try:
        process = subprocess.run(
            "docker ps --filter ancestor=frontend --format {{.ID}}",
            shell=True,
            check=True,
            text=True,
            capture_output=True
        )
        return process.stdout.strip()
    except subprocess.CalledProcessError:
        return None

def start_services():
    """
    Start both server and frontend services
    """
    # Start server
    server_path = "./server"
    if not os.path.exists(server_path):
        print(f"Error: {server_path} directory not found!")
        return False

    print("\n=== Starting Server ===")
    if not run_command("docker compose up -d", cwd=server_path):
        return False

    # Start frontend
    frontend_path = "./frontend"
    if not os.path.exists(frontend_path):
        print(f"Error: {frontend_path} directory not found!")
        return False

    print("\n=== Starting Frontend ===")
    # Build frontend image
    if not run_command("docker build -t frontend .", cwd=frontend_path):
        return False
    
    # Run frontend container
    if not run_command("docker run -d -p 4173:4173 frontend", cwd=frontend_path):
        return False

    return True

def stop_services():
    """
    Stop all running containers and remove images
    """
    print("\n=== Stopping Services ===")
    
    # Stop server containers
    server_path = "./server"
    if os.path.exists(server_path):
        print("Stopping server containers...")
        run_command("docker compose down", cwd=server_path)
    
    # Stop frontend container
    print("Stopping frontend container...")
    container_id = get_frontend_container_id()
    if container_id:
        # Stop the container
        run_command(f"docker stop {container_id}")
        # Remove the container
        run_command(f"docker rm {container_id}")
        # Remove the frontend image
        run_command("docker rmi frontend")
        print("Frontend container and image removed")
    else:
        print("No frontend container found running")
        # Try to remove the image if it exists
        run_command("docker rmi frontend")
    
    print("All services stopped and cleaned up")
    return True

def main():
    parser = argparse.ArgumentParser(description='Manage Docker services')
    parser.add_argument('action', choices=['start', 'stop'], help='Action to perform (start or stop)')
    
    args = parser.parse_args()
    
    if args.action == 'start':
        if start_services():
            print("\nAll services started successfully!")
        else:
            print("\nError starting services")
            sys.exit(1)
    elif args.action == 'stop':
        stop_services()

if __name__ == "__main__":
    main()