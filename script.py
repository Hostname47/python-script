#!/usr/bin/env python3
"""
Simple build script for Jenkins pipeline
"""

import os
import sys
import subprocess
import json
from datetime import datetime

def log_message(message, level="INFO"):
    """Log message with timestamp"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{timestamp}] {level}: {message}")

def run_command(command, check=True):
    """ Execute shell command and return result """
    log_message(f"Executing: {command}")
    try:
        result = subprocess.run(
            command, 
            shell=True, 
            capture_output=True, 
            text=True, 
            check=check
        )
        if result.stdout:
            log_message(f"Output: {result.stdout.strip()}")
        return result
    except subprocess.CalledProcessError as e:
        log_message(f"Command failed with exit code {e.returncode}", "ERROR")
        log_message(f"Error output: {e.stderr}", "ERROR")
        raise

def get_build_info():
    """Get build information from environment variables"""
    build_info = {
        "build_number": os.getenv("BUILD_NUMBER", "unknown"),
        "job_name": os.getenv("JOB_NAME", "unknown"),
        "build_url": os.getenv("BUILD_URL", "unknown"),
        "workspace": os.getenv("WORKSPACE", os.getcwd()),
        "git_commit": os.getenv("GIT_COMMIT", "unknown"),
        "git_branch": os.getenv("GIT_BRANCH", "unknown")
    }
    return build_info

def create_build_artifact():
    """Create a simple build artifact"""
    build_info = get_build_info()
    artifact_data = {
        "build_timestamp": datetime.now().isoformat(),
        "build_info": build_info,
        "status": "success"
    }
    
    artifact_path = "build_artifact.json"
    with open(artifact_path, 'w') as f:
        json.dump(artifact_data, f, indent=2)
    
    log_message(f"Created build artifact: {artifact_path}")
    return artifact_path

def main():
    """Main build function"""
    log_message("Starting build process")
    
    try:
        # Print build information
        build_info = get_build_info()
        log_message("Build Information:")
        for key, value in build_info.items():
            log_message(f"  {key}: {value}")
        
        # Example build steps - customize as needed
        log_message("Running build steps...")
        
        # Step 1: Check Python version
        run_command("python3 --version")
        
        # Step 2: Install dependencies (if requirements.txt exists)
        if os.path.exists("requirements.txt"):
            log_message("Installing Python dependencies...")
            run_command("pip install -r requirements.txt")
        
        # Step 3: Run tests (if test files exist)
        if any(f.startswith("test_") and f.endswith(".py") for f in os.listdir(".")):
            log_message("Running tests...")
            run_command("python3 -m pytest -v", check=False)
        
        # Step 4: Create build artifact
        artifact_path = create_build_artifact()
        
        log_message("Build completed successfully!")
        return 0
        
    except Exception as e:
        log_message(f"Build failed: {str(e)}", "ERROR")
        return 1

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
