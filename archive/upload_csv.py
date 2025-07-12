CSV_FILE = "pantry_master.csv"

def load_existing_csv_items():
    existing_items = set()
    if os.path.exists(CSV_FILE):
        with open(CSV_FILE, mode="r", newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                existing_items.add(row["item"].lower())
    return existing_items


def update_csv(pantry_list):
    existing_items = load_existing_csv_items()
    added_items = set(existing_items)  # So we can update during loop

    new_rows = []
    for row in pantry_list:
        item_lower = row["item"].strip().lower()
        if item_lower not in added_items:
            new_rows.append(row)
            added_items.add(item_lower)  # Track this as added

    if new_rows:
        file_exists = os.path.exists(CSV_FILE)
        with open(CSV_FILE, mode="a", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=["item", "category"])
            if not file_exists:
                writer.writeheader()
            writer.writerows(new_rows)