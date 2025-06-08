#!/usr/bin/env python3
"""
Script to test the APIs independently
"""

import subprocess
import sys
import time
from datetime import datetime
from pathlib import Path

import requests


def log(method, message):
    now = datetime.now().strftime("%H:%M:%S")
    print(f"[{method} {now}][{message}]")


def test_rest_api():
    """Tests the REST API independently"""
    method = "test_rest_api"
    log(method, "Starting REST API test")

    try:
        process = subprocess.Popen([sys.executable, "apis/rest_api.py"],
                                   stdout=subprocess.PIPE,
                                   stderr=subprocess.PIPE,
                                   text=True)

        log(method, f"REST API started, PID: {process.pid}")

        time.sleep(3)

        if process.poll() is not None:
            stdout, stderr = process.communicate()
            log(method, "REST API exited unexpectedly")
            log(method, f"STDOUT: {stdout.strip()}")
            log(method, f"STDERR: {stderr.strip()}")
            return False

        try:
            response = requests.get("http://localhost:5000/api/post/simple/1", timeout=5)
            log(method, f"REST API responded with status: {response.status_code}")
            log(method, f"Response: {response.json()}")
        except Exception as e:
            log(method, f"Error connecting to REST API: {e}")
            return False
        finally:
            process.terminate()
            process.wait()

        return True

    except Exception as e:
        log(method, f"Error testing REST API: {e}")
        return False


def test_graphql_api():
    """Tests the GraphQL API independently"""
    method = "test_graphql_api"
    log(method, "Starting GraphQL API test")

    try:
        process = subprocess.Popen([sys.executable, "apis/graphql_api.py"],
                                   stdout=subprocess.PIPE,
                                   stderr=subprocess.PIPE,
                                   text=True)

        log(method, f"GraphQL API started, PID: {process.pid}")

        time.sleep(3)

        if process.poll() is not None:
            stdout, stderr = process.communicate()
            log(method, "GraphQL API exited unexpectedly")
            log(method, f"STDOUT: {stdout.strip()}")
            log(method, f"STDERR: {stderr.strip()}")
            return False

        try:
            query = {
                "query": """
                query {
                    postSimple(postId: 1) {
                        title
                        author {
                            name
                        }
                    }
                }
                """
            }
            response = requests.post("http://localhost:5001/graphql", json=query, timeout=5)
            log(method, f"GraphQL API responded with status: {response.status_code}")
            log(method, f"Response: {response.json()}")
        except Exception as e:
            log(method, f"Error connecting to GraphQL API: {e}")
            return False
        finally:
            process.terminate()
            process.wait()

        return True

    except Exception as e:
        log(method, f"Error testing GraphQL API: {e}")
        return False


def check_database():
    """Checks if the database file exists"""
    method = "check_database"
    log(method, "Checking for database file")

    db_paths = [
        "database/blog.db",
        "apis/blog.db",
        "blog.db"
    ]

    for db_path in db_paths:
        if Path(db_path).exists():
            log(method, f"Database found at: {db_path}")
            return True

    log(method, "Database not found")
    log(method, "Run: python3 database/database.py")
    return False


def main():
    method = "main"
    log(method, "Manual API test started")
    print("=" * 40)

    if not check_database():
        return

    rest_ok = test_rest_api()
    graphql_ok = test_graphql_api()

    print("\n" + "=" * 40)
    log(method, "TEST RESULTS")
    log(method, f"REST API: {'OK' if rest_ok else 'FAILED'}")
    log(method, f"GraphQL API: {'OK' if graphql_ok else 'FAILED'}")


if __name__ == "__main__":
    main()
