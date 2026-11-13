import json
import time
from pathlib import Path
from dotenv import load_dotenv
from src.extractor import get_client, extract_ticket

BASE_DIR = Path(__file__).resolve().parent
MODEL_NAME = "gemini-3.5-flash-lite"
PROMPT_VERSION = "v1_baseline"


def main() -> None:
    load_dotenv(BASE_DIR / ".env")
    results_dir = BASE_DIR / "results"
    results_dir.mkdir(exist_ok=True)

    system_prompt = (BASE_DIR / "prompts" / f"{PROMPT_VERSION}.txt").read_text(encoding="utf-8")
    tickets = json.loads((BASE_DIR / "data" / "tickets.json").read_text(encoding="utf-8"))

    client = get_client()
    results = []

    for ticket in tickets:
        print(f"Processing {ticket['id']}...")
        extracted = extract_ticket(
            client=client,
            system_prompt=system_prompt,
            raw_text=ticket["text"],
            model=MODEL_NAME,
        )
        results.append({
            "id": ticket["id"],
            "model": MODEL_NAME,
            "prompt_version": PROMPT_VERSION,
            "output": extracted,
        })
        time.sleep(0.5)

    out_path = results_dir / f"{PROMPT_VERSION}_{MODEL_NAME}.json"
    out_path.write_text(json.dumps(results, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Done! Saved {len(results)} records to {out_path}")


if __name__ == "__main__":
    main()