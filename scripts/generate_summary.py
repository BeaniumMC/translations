import os
import json

SOURCES_DIR = "sources"
TRANSLATIONS_DIR = "translations"
OUTPUT_FILE = "public/summary.json"
LANGUAGES_FILE = "languages.json"

os.makedirs(os.path.dirname(OUTPUT_FILE), exist_ok=True)

summary = {}

# Load languages from languages.json keys
with open(LANGUAGES_FILE, encoding="utf-8") as lang_file:
    languages_data = json.load(lang_file)
    languages = list(languages_data.keys())

source_files = [f for f in os.listdir(SOURCES_DIR) if f.endswith(".json")]

for source_file in source_files:
    with open(os.path.join(SOURCES_DIR, source_file), encoding="utf-8") as f:
        source_data = json.load(f)

    source_keys = list(source_data.keys())
    summary[source_file] = {
        "total": len(source_keys),
        "keys": source_keys,
        "translations": {}
    }

    for lang in languages:
        translation_path = os.path.join(TRANSLATIONS_DIR, lang, source_file)
        try:
            with open(translation_path, encoding="utf-8") as tf:
                translation_data = json.load(tf)
        except (FileNotFoundError, json.JSONDecodeError):
            translation_data = {}

        missing = [k for k in source_keys if k not in translation_data or not translation_data[k].strip()]
        translated = len(source_keys) - len(missing)
        percent = int((translated / len(source_keys)) * 100) if source_keys else 0

        summary[source_file]["translations"][lang] = {
            "completed": translated,
            "missing": missing,
            "percent": percent
        }

with open(OUTPUT_FILE, "w", encoding="utf-8") as out:
    json.dump(summary, out, indent=2, ensure_ascii=False)

print(f"✅ Summary written to {OUTPUT_FILE}")
