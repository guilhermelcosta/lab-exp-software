import csv
import os
import time
from datetime import datetime

import requests

REST_BASE_URL = "http://localhost:5000/api"
GRAPHQL_BASE_URL = "http://localhost:5001/graphql"

OUTPUT_DIR = "../data"
os.makedirs(OUTPUT_DIR, exist_ok=True)

GRAPHQL_QUERIES = {
    "simple": """
    query {
        postSimple(postId: 1) {
            title
            author {
                name
            }
        }
    }
    """,
    "medium": """
    query {
        postMedium(postId: 1) {
            title
            content
            comments {
                content
            }
        }
    }
    """,
    "complex": """
    query {
        postComplex(postId: 1) {
            id
            title
            content
            author {
                id
                name
                email
            }
            comments {
                id
                content
                author {
                    name
                }
                timestamp
            }
        }
    }
    """
}


def run_benchmark():
    results = []

    for api_type in ['REST', 'GraphQL']:
        for complexity in ['simple', 'medium', 'complex']:
            for i in range(30):
                start_time = time.time()

                if api_type == 'REST':
                    url = f"{REST_BASE_URL}/post/{complexity}/1"
                    response = requests.get(url)
                else:
                    response = requests.post(
                        GRAPHQL_BASE_URL,
                        json={'query': GRAPHQL_QUERIES[complexity]}
                    )

                elapsed = (time.time() - start_time) * 1000  # ms
                size = len(response.content)  # bytes

                results.append({
                    'api': api_type,
                    'complexity': complexity,
                    'execution': i + 1,
                    'time_ms': round(elapsed, 2),
                    'size_bytes': size,
                    'timestamp': datetime.now().isoformat()
                })

                print(f"{api_type} {complexity} run {i + 1}: {elapsed:.2f}ms, {size} bytes")

    with open(f"{OUTPUT_DIR}/results.csv", 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=results[0].keys())
        writer.writeheader()
        writer.writerows(results)


if __name__ == '__main__':
    run_benchmark()
