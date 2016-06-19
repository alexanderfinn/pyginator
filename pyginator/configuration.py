import os


class Configuration(object):

    """
        pyginator configuration representation
        settings is a dict loaded from configuration file
    """
    def __init__(self, base_path, settings):
        self.base_path = base_path
        self.templates_dir = settings.get("templates_dir", "templates")
        self.source_dir = settings.get("source_dir", "src")
        self.target_dir = settings.get("target_dir", "target")
        self.data_dir = settings.get("data_dir", "data")
        self.fields = settings.get("fields", {})
        self.pretty_urls = settings.get("pretty_urls", None) == 'True' and True or False
        self.static_folders = settings.get("static_folders", [])
        self.s3bucket = settings.get("s3bucket", None)
        self.scripts_dir = settings.get("scripts_dir", "scripts")

    @property
    def templates_abs_path(self):
        return os.path.join(self.base_path, self.templates_dir)

    @property
    def sources_abs_path(self):
        return os.path.join(self.base_path, self.source_dir)

    @property
    def target_path(self):
        return os.path.join(self.base_path, self.target_dir)

    @property
    def data_path(self):
        return os.path.join(self.base_path, self.data_dir)

    @property
    def scripts_abs_path(self):
        return os.path.join(self.base_path, self.scripts_dir)
    
    

    