#!/usr/bin/env python3

import os
import signal
import subprocess
import sys
import time
from pathlib import Path

BASE_DIR = Path(__file__).parent
API_DIR = BASE_DIR / "apis"
DATABASE_DIR = BASE_DIR / "database"
BENCHMARK_DIR = BASE_DIR / "benchmark"
ANALYSIS_DIR = BASE_DIR / "analysis"


def log(method, message):
    timestamp = time.strftime("%H:%M:%S")
    print(f"[{method} {timestamp}][{message}]")


class ExperimentRunner:
    def __init__(self):
        self.processes = []
        self.running = True

    def run_script(self, script_path, cwd=None, wait=True):
        method = "run_script"
        log(method, f"Running: {script_path}")
        try:
            if wait:
                result = subprocess.run([sys.executable, script_path],
                                        cwd=cwd,
                                        capture_output=True,
                                        text=True)
                if result.returncode != 0:
                    log(method, f"Error while executing {script_path}")
                    log(method, result.stderr.strip())
                    return False
                else:
                    log(method, f"{script_path} executed successfully")
                    if result.stdout:
                        log(method, f"Output: {result.stdout.strip()}")
                return True
            else:
                process = subprocess.Popen([sys.executable, script_path],
                                           cwd=cwd,
                                           stdout=subprocess.PIPE,
                                           stderr=subprocess.PIPE,
                                           text=True)
                self.processes.append(process)
                return process
        except Exception as e:
            log(method, f"Exception while executing {script_path}: {e}")
            return False

    def wait_for_api(self, url, timeout=30):
        method = "wait_for_api"
        import requests
        log(method, f"Waiting for API at {url}")

        start_time = time.time()
        while time.time() - start_time < timeout:
            try:
                response = requests.get(url, timeout=5)
                if response.status_code == 200:
                    log(method, f"API available at {url}")
                    return True
            except requests.exceptions.RequestException:
                pass
            time.sleep(1)

        log(method, f"Timeout: API not available at {url}")
        return False

    def wait_for_graphql_api(self, url, timeout=30):
        method = "wait_for_graphql_api"
        import requests
        log(method, f"Waiting for GraphQL API at {url}")

        start_time = time.time()
        while time.time() - start_time < timeout:
            try:
                query = {"query": "{ __schema { types { name } } }"}
                response = requests.post(url, json=query, timeout=5)
                if response.status_code in [200, 400]:
                    log(method, f"GraphQL API available at {url}")
                    return True
            except requests.exceptions.RequestException:
                pass
            time.sleep(1)

        log(method, f"Timeout: GraphQL API not available at {url}")
        return False

    def cleanup(self):
        method = "cleanup"
        log(method, "Shutting down processes")
        for process in self.processes:
            try:
                if process.poll() is None:
                    process.terminate()
                    try:
                        process.wait(timeout=5)
                    except subprocess.TimeoutExpired:
                        process.kill()
                        process.wait()
            except Exception as e:
                log(method, f"Error while terminating process: {e}")
        self.processes.clear()

    def signal_handler(self, signum, frame):
        method = "signal_handler"
        log(method, "Interrupt signal received")
        self.running = False
        self.cleanup()
        sys.exit(0)

    def check_api_errors(self, process, api_name):
        method = "check_api_errors"
        if process.poll() is not None:
            stdout, stderr = process.communicate()
            if stderr:
                log(method, f"Error in {api_name}")
                log(method, stderr.strip())
            return False
        return True

    def run_experiment(self):
        method = "run_experiment"
        signal.signal(signal.SIGINT, self.signal_handler)

        log(method, "Starting GraphQL vs REST experiment")

        try:
            log(method, "Step 1: Initializing database")
            db_path = DATABASE_DIR / "blog.db"
            if db_path.exists():
                log(method, f"Database already exists at {db_path}, skipping initialization")
            else:
                if not self.run_script("database.py", cwd=DATABASE_DIR):
                    return False

            log(method, "Step 2: Starting APIs")

            log(method, "Starting REST API")
            rest_process = self.run_script("rest_api.py", cwd=API_DIR, wait=False)
            if not rest_process:
                return False
            time.sleep(3)
            if not self.check_api_errors(rest_process, "REST API"):
                return False
            if not self.wait_for_api("http://localhost:5000/api/post/simple/1"):
                return False

            log(method, "Starting GraphQL API")
            graphql_process = self.run_script("graphql_api.py", cwd=API_DIR, wait=False)
            if not graphql_process:
                return False
            time.sleep(3)
            if not self.check_api_errors(graphql_process, "GraphQL API"):
                return False
            if not self.wait_for_graphql_api("http://localhost:5001/graphql"):
                return False

            log(method, "Step 3: Running benchmark")
            if not self.run_script("benchmark.py", cwd=BENCHMARK_DIR):
                return False

            log(method, "Step 4: Running analysis")
            if not self.run_script("analysis.py", cwd=ANALYSIS_DIR):
                return False

            log(method, "Experiment completed successfully")
        except Exception as e:
            log(method, f"Error during experiment: {e}")
            return False
        finally:
            self.cleanup()

        return True


def check_requirements():
    method = "check_requirements"
    required_files = [
        DATABASE_DIR / "database.py",
        API_DIR / "rest_api.py",
        API_DIR / "graphql_api.py",
        BENCHMARK_DIR / "benchmark.py",
        ANALYSIS_DIR / "analysis.py"
    ]

    missing_files = [str(file_path) for file_path in required_files if not file_path.exists()]

    if missing_files:
        log(method, "Required files not found:")
        for file in missing_files:
            log(method, f"Missing: {file}")
        return False

    return True


def main():
    method = "main"
    log(method, "Checking project structure")

    if not check_requirements():
        log(method, "Please ensure all files are correctly placed:")
        log(method, "Expected:")
        log(method, " - database/database.py")
        log(method, " - apis/rest_api.py")
        log(method, " - apis/graphql_api.py")
        log(method, " - benchmark/benchmark.py")
        log(method, " - analysis/analysis.py")
        return

    log(method, "Project structure verified")

    os.makedirs("data", exist_ok=True)
    os.makedirs("reports", exist_ok=True)

    runner = ExperimentRunner()
    success = runner.run_experiment()

    if success:
        log(method, "EXPERIMENT COMPLETED SUCCESSFULLY")
    else:
        log(method, "EXPERIMENT FAILED")


if __name__ == "__main__":
    main()
