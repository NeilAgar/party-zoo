from dynaconf import Dynaconf

settings = Dynaconf(
    settings_files=['settings.toml', '.secrets.toml'],
)


def get_config():
    return settings.controller_count, list(settings.aspect_ratio)
