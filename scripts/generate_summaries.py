import os
import json

import badges

from common import *

GITHUB_REPO = f"{GITHUB_REPO_URL}/blob/main"
OUTPUT_DIR = os.path.join(PUBLIC_DIR, 'summary')

os.makedirs(OUTPUT_DIR, exist_ok=True)

projects = load_projects()

for project in projects:
    output_file = os.path.join(OUTPUT_DIR, f"{project.id}.json")

    summary = {
        'files': {}
    }
    missing_total = 0

    # Load languages from languages.json keys
    with open(project.get_languages_file(), encoding='utf-8') as lang_file:
        languages_data = json.load(lang_file)
        languages = list(languages_data.keys())

    source_files = [f for f in os.listdir(project.get_sources_dir()) if f.endswith('.json')]

    for source_file in source_files:
        with open(os.path.join(project.get_sources_dir(), source_file), encoding='utf-8') as f:
            source_data = json.load(f)

        source_keys = list(source_data.keys())
        file_summary = {
            'total': len(source_keys),
            'keys': source_keys,
            'url': f"{GITHUB_REPO}/{project.get_sources_dir()}/{source_file}",
            'translations': {}
        }

        for lang in languages:
            translation_path = os.path.join(project.get_translations_dir(), lang, source_file)
            try:
                with open(translation_path, encoding='utf-8') as tf:
                    translation_data = json.load(tf)
            except (FileNotFoundError, json.JSONDecodeError):
                translation_data = {}

            missing = [k for k in source_keys if k not in translation_data or not translation_data[k].strip()]
            missing_total += len(missing)
            translated = len(source_keys) - len(missing)
            percent = int((translated / len(source_keys)) * 100) if source_keys else 0

            file_summary['translations'][lang] = {
                'completed': translated,
                'missing': missing,
                'percent': percent,
                'url': f"{GITHUB_REPO}/{project.get_translations_dir()}/{lang}/{source_file}"
            }

        summary['files'][source_file] = file_summary

    summary['missing_total'] = missing_total

    with open(output_file, 'w', encoding='utf-8') as out:
        json.dump(summary, out, indent=2, ensure_ascii=False)

    print(f"✅ Summary of {project.name} written to {output_file}")

badges.create_badges(missing_total, len(projects))
