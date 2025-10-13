import json
import os

from common import *

OUTPUT_DIR = os.path.join(PUBLIC_DIR, 'badges')

def create_badge(label: str, message: str, color: str, path: str):
    badge_data = {
        'schemaVersion': 1,
        'label': label,
        'message': message,
        'color': color
    }

    os.makedirs(OUTPUT_DIR, exist_ok=True)

    with open(os.path.join(OUTPUT_DIR, path), 'w') as f:
        json.dump(badge_data, f)


def create_badges(missing_total: int, projects: int):
    create_badge('Missing strings', str(missing_total), 'green' if missing_total == 0 else 'red', 'missing_strings.json')
    create_badge('Projects', str(projects), 'blue', 'projects.json')
