# scripts/prepare_data.py
import json
import re
from pathlib import Path
from datasets import load_dataset


def anonymize(text: str) -> str:
    text = re.sub(r"[\w\.-]+@[\w\.-]+\.\w+", "[EMAIL]", text)
    text = re.sub(r"\+?\d[\d\s\-]{7,}\d", "[PHONE]", text)
    return text.strip()


def main() -> None:
    Path("data").mkdir(exist_ok=True)
    ds = load_dataset("Tobi-Bueck/customer-support-tickets", split="train", streaming=True)

    short_tickets, medium_tickets, long_tickets = [], [], []

    for row in ds:
        subject = row.get("subject") or ""
        body = row.get("body") or ""
        raw_text = anonymize(f"Subject: {subject}\n{body}" if subject else body)

        item = {
            "raw_text": raw_text,
            "hf_hints": {  # Підказки з датасету, які допоможуть вам при розмітці golden set
                "language": row.get("language"),
                "type": row.get("type"),
                "queue": row.get("queue"),
                "priority": row.get("priority"),
            },
        }

        length = len(raw_text)
        if 40 <= length < 160 and len(short_tickets) < 10:
            short_tickets.append(item)
        elif 160 <= length < 450 and len(medium_tickets) < 10:
            medium_tickets.append(item)
        elif length >= 450 and len(long_tickets) < 10:
            long_tickets.append(item)

        if len(short_tickets) == 10 and len(medium_tickets) == 10 and len(long_tickets) == 10:
            break

    all_tickets = short_tickets + medium_tickets + long_tickets
    for idx, t in enumerate(all_tickets, start=1):
        t["id"] = f"ticket_{idx:02d}"

    # 1. Зберігаємо 30 сирих текстів (без підказок)
    clean_input = [{"id": t["id"], "text": t["raw_text"]} for t in all_tickets]
    Path("../data/tickets.json").write_text(
        json.dumps(clean_input, ensure_ascii=False, indent=2), encoding="utf-8"
    )

    # 2. Беремо по 3-4 тікети з кожної групи довжини для ручної розмітки golden set (разом 10)
    golden_candidates = short_tickets[:4] + medium_tickets[:3] + long_tickets[:3]
    golden_template = [
        {
            "id": t["id"],
            "text": t["raw_text"],
            "hf_hints_delete_after_labeling": t["hf_hints"],
            "expected": {
                "language": t["hf_hints"]["language"] or "en",
                "ticket_type": "incident",
                "priority": "medium",
                "department": "Technical Support",
                "summary": "TODO: 1 sentence summary in English",
                "technical_context": {
                    "affected_system": None,
                    "error_code": None,
                    "steps_already_tried": [],
                },
                "requires_human_escalation": False,
            },
        }
        for t in golden_candidates
    ]
    Path("../data/golden_set.json").write_text(
        json.dumps(golden_template, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    print("Готово! Перевірте data/tickets.json і вручну заповніть expected у data/golden_set.json.")


if __name__ == "__main__":
    main()
