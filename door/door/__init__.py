"""Main entry point
"""
from pyramid.config import Configurator
from pyramid_beaker import session_factory_from_settings
from pyramid_beaker import set_cache_regions_from_settings

from pyramid.threadlocal import get_current_registry


def main(global_config, **settings):
    sessionFactory = session_factory_from_settings(settings)
    set_cache_regions_from_settings(settings)
    config = Configurator(settings=settings)
    config.set_session_factory(sessionFactory)

    get_current_registry().settings = settings
    config = Configurator(settings=settings)
    config.include("cornice")
    config.include('pyramid_beaker')
    config.scan("door.views")
    return config.make_wsgi_app()
