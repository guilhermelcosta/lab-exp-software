# General config
STANDART_TIMEOUT=5

# Repository setup
FIELD_NAMES=["name", "stargazerCount", "owner", "createdAt", "updatedAt", "releases", "url"]

# Github config
GITHUB_URL="https://api.github.com/graphql"
AUTHORIZATION="Authorization"

# Directories
RESULTS_DIR="results"
REPOSITORIES_DIR="repositories"
CK_RESULTS_DIR= "ck_results"

# Files
REPOSITORIES_FILE="repositories.csv"
FAILED_CLONES_FILE="failed_clones.csv"
MISSING_CK_FILE="missing_ck_files.csv"
SUMMARY_CK_FILE="summary_ck.csv"

# CK
CK_GENERATED_FILES=["class.csv", "method.csv", "field.csv", "variable.csv"]