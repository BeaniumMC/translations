import json
import os

from common import PUBLIC_DIR

OUTPUT_DIR = os.path.join(PUBLIC_DIR, 'badges')

os.makedirs(OUTPUT_DIR, exist_ok=True)

def create_badge(label: str, message: str, color: str, path: str) -> dict:
    badge_data = {
        'schemaVersion': 1,
        'label': label,
        'message': message,
        'color': color
    }

    with open(os.path.join(OUTPUT_DIR, path), 'w') as f:
        json.dump(badge_data, f)

    return badge_data


def create_badges(missing_total: int, projects: int) -> None:
    create_badge('Missing strings', str(missing_total), 'green' if missing_total == 0 else 'red', 'missing_strings.json')
    create_badge('Projects', str(projects), 'blue', 'projects.json')
