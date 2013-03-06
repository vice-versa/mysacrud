from pyramid.config import Configurator
from sqlalchemy import engine_from_config

from models import DBSession, Base
from models import MyModel


def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    engine = engine_from_config(settings, 'sqlalchemy.')
    DBSession.configure(bind=engine)
    Base.metadata.bind = engine
    config = Configurator(settings=settings)
    config.add_static_view('static', 'static', cache_max_age=3600)
    config.add_route('home', '/')
    # pyramid_jinja2 configuration
    config.include('pyramid_jinja2')
    config.include('sacrud.pyramid_ext')
    settings = config.registry.settings
    settings['sacrud_models'] = (MyModel,)
    config.scan()
    
    return config.make_wsgi_app()
