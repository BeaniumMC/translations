import os
import json
import zipfile

from common import *

OUTPUT_DIR = './exports'

os.makedirs(OUTPUT_DIR, exist_ok=True)

def compute_language_progress(project, languages):
    """Return progress + per-file progress for each language."""
    result = {}

    sources_dir = project.get_sources_dir()
    translations_dir = project.get_translations_dir()
    source_files = [f for f in os.listdir(sources_dir) if f.endswith('.json')]

    for lang in languages:
        lang_id = lang.id
        lang_progress = {
            'progress': 0.0,
            'file_progress': {},
            'translators': lang.translators,  # copy from main languages.json
        }

        total_keys = 0
        total_translated = 0

        for source_file in source_files:
            with open(os.path.join(sources_dir, source_file), encoding='utf-8') as f:
                source_data = json.load(f)

            source_keys = list(source_data.keys())
            total_keys += len(source_keys)

            translation_path = os.path.join(translations_dir, lang_id, source_file)

            try:
                with open(translation_path, encoding='utf-8') as tf:
                    translation_data = json.load(tf)
            except (FileNotFoundError, json.JSONDecodeError):
                translation_data = {}

            translated = sum(
                1 for k in source_keys if k in translation_data and translation_data[k].strip()
            )

            # file-level progress (0–1 float)
            file_pct = translated / len(source_keys) if source_keys else 0
            lang_progress['file_progress'][source_file] = file_pct

            total_translated += translated

        # global language progress (0–1 float)
        lang_progress['progress'] = total_translated / total_keys if total_keys else 0

        result[lang_id] = lang_progress

    return result


for project in load_projects():
    zip_name = f"translations-{project.id}.zip"
    zip_path = os.path.join(OUTPUT_DIR, zip_name)

    translations_dir = project.get_translations_dir()

    # Load main repo languages.json (original format — stays untouched)
    languages_file = os.path.join(translations_dir, 'languages.json')
    with open(languages_file, encoding='utf-8') as f:
        raw_languages = json.load(f)

    # Convert raw languages to lang objects from project.get_languages()
    languages = project.get_languages()

    # Compute new languages.json with progress
    new_lang_json = compute_language_progress(project, languages)

    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        # Write all translation files
        for root, _, files in os.walk(translations_dir):
            for file in files:
                if file.endswith('.json') and file != 'languages.json':
                    full_path = os.path.join(root, file)
                    arcname = os.path.relpath(full_path, translations_dir)
                    zipf.write(full_path, arcname)

        # Write the **new transformed languages.json**
        zipf.writestr('languages.json', json.dumps(new_lang_json, indent=2, ensure_ascii=False))

    print(f"📦 Exported {zip_name}")
