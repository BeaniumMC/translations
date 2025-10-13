import os
import re
import json
import sys

from common import *

def extract_placeholders(text):
    return sorted(set(PLACEHOLDER_REGEX.findall(text or '')))

def lint_file(source_path: str, translation_path: str, project: Project, lang: str, filename: str) -> list:
    errors = []

    file_path = f"{project.id}/{lang}/{filename}"

    with open(source_path, encoding='utf-8') as sf:
        try:
            source_data = json.load(sf)
        except json.JSONDecodeError as e:
            errors.append({
                'type': 'invalid_json',
                'file': file_path,
                'message': f"Source JSON is invalid: {e}"
            })
            return errors

    try:
        with open(translation_path, encoding='utf-8') as tf:
            translation_data = json.load(tf)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        errors.append({
            'type': 'missing_or_invalid',
            'file': file_path,
            'message': f"Translation file missing or invalid: {e}"
        })
        return errors

    source_keys = set(source_data.keys())
    translation_keys = set(translation_data.keys())

    # Check for missing, empty, and mismatched placeholders
    for key in source_keys:
        source_val = source_data.get(key, '')
        trans_val = translation_data.get(key, '')

        if trans_val.strip() == '':
            errors.append({
                'type': 'empty_string',
                'file': file_path,
                'key': key,
                'message': 'Translation is empty'
            })

        source_ph = extract_placeholders(source_val)
        trans_ph = extract_placeholders(trans_val)

        if source_ph != trans_ph:
            errors.append({
                'type': 'placeholder_mismatch',
                'file': file_path,
                'key': key,
                'source_placeholders': source_ph,
                'translation_placeholders': trans_ph,
                'message': 'Placeholders do not match'
            })

    # Check for unused (extra) keys in translation
    extra_keys = translation_keys - source_keys
    for key in extra_keys:
        errors.append({
            'type': 'unused_key',
            'file': file_path,
            'key': key,
            'message': 'Key does not exist in source'
        })

    return errors


def main():
    failed = False
    all_errors = []

    for project in load_projects():
        languages = [d for d in os.listdir(project.get_translations_dir()) if os.path.isdir(os.path.join(project.get_translations_dir(), d))]
        source_files = [f for f in os.listdir(project.get_sources_dir()) if f.endswith('.json')]

        for filename in source_files:
            source_path = os.path.join(project.get_sources_dir(), filename)

            for lang in languages:
                translation_path = os.path.join(project.get_translations_dir(), lang, filename)
                errors = lint_file(source_path, translation_path, project, lang, filename)
                all_errors.extend(errors)

    if all_errors:
        print('❌ Linting issues found:\n')
        for err in all_errors:
            print(f"🔹 [{err['type']}] {err['file']} → `{err.get('key', '')}`")
            print(f"    {err['message']}")
            if err['type'] == 'placeholder_mismatch':
                print(f"    Source PHs: {err['source_placeholders']}")
                print(f"    Trans PHs:  {err['translation_placeholders']}")
            print()
        sys.exit(1)
    else:
        print('✅ All translations passed linting.')

if __name__ == '__main__':
    main()
