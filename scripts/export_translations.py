import os
import zipfile

from common import *

OUTPUT_DIR = './exports'

os.makedirs(OUTPUT_DIR, exist_ok=True)

for project in load_projects():
    zip_name = f"translations-{project.id}.zip"
    zip_path = os.path.join(OUTPUT_DIR, zip_name)

    translations_dir = project.get_translations_dir()

    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, _, files in os.walk(translations_dir):
            for file in files:
                if file.endswith('.json'):
                    full_path = os.path.join(root, file)
                    arcname = os.path.relpath(full_path, translations_dir)
                    zipf.write(full_path, arcname)
