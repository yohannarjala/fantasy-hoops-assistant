set -euo pipefail

REPO="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$REPO"

mkdir -p reports logs
source .venv/bin/activate
python src/main.py 2>&1 | tee -a "logs/$(date +%F).log"
