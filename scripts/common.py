GITHUB_REPO_URL = 'https://github.com/BeaniumMC/translations'
PUBLIC_DIR = 'public'
SOURCES_DIR = 'sources'
TRANSLATIONS_DIR = 'translations'
PROJECTS_FILE = os.path.join(SOURCES_DIR, 'projects.json')
PLACEHOLDER_REGEX = re.compile(r"%(\d+\$)?[sd]")

class Project:
    def __init__(self, data: dict):
        self.id = data['id']
        self.name = data['name']
        self.description = data['description']

    def get_sources_dir(self) -> str:
        return os.path.join(SOURCES_DIR, self.id)

    def get_translations_dir(self) -> str:
        return os.path.join(TRANSLATIONS_DIR, self.id)

    def get_languages_file(self) -> str:
        return os.path.join(self.get_translations_dir(), 'languages.json')

@staticmethod
def load_projects() -> list[Project]:
    projects = []
    with open(PROJECTS_FILE, encoding='utf-8') as f:
        project_list = json.load(f)
        for project_data in project_list['projects']:
            projects.append(Project(project_data))
    return projects