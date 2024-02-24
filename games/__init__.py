"""Initialize Flask app."""

from flask import Flask, render_template
import games.adapters.repository as repo
from games.adapters.database_repository import SqlAlchemyRepository
from pathlib import Path
#

from sqlalchemy import create_engine, inspect
from sqlalchemy.orm import sessionmaker, clear_mappers
from sqlalchemy.pool import NullPool

from games.adapters.memory_repository import MemoryRepository
from games.adapters.orm import metadata, map_model_to_tables
from games.adapters import memory_repository, database_repository
#

def create_app(test_config=None):
    """Construct the core application."""

    # Create the Flask app object.
    app = Flask(__name__)
    app.config.from_object('config.Config')
    #database implementation

    if test_config is not None:
        app.config['REPOSITORY'] = 'memory'

    if app.config['REPOSITORY'] == 'database':
        database_uri = app.config['SQLALCHEMY_DATABASE_URI']
        database_echo = app.config['SQLALCHEMY_ECHO']

        database_engine = create_engine(database_uri, connect_args={"check_same_thread": False},
                                    poolclass=NullPool, echo=database_echo)

        session_factory = sessionmaker(autocommit=False, autoflush=True, bind=database_engine)

        repo.repo_instance = SqlAlchemyRepository(session_factory)

        #database implementation
        app.config.from_object('config.Config')
        data_path = Path('games') / 'adapters' / 'data'

        #database implementation
        if len(inspect(database_engine).get_table_names()) == 0:
            print("REPOPULATING DATABASE... STARTED")
            # reset all metadata / mappers that may cause errors?
            clear_mappers()
            metadata.create_all(database_engine)
            for table in reversed(metadata.sorted_tables):
                with database_engine.connect() as conn:
                    conn.execute(table.delete())

            map_model_to_tables()

            repo.repo_instance.populate(data_path)
            print("REPOPULATING DATABASE... FINISHED")
        else:
            map_model_to_tables()

        #database implementation
    elif app.config['REPOSITORY'] == 'memory':
        #  Create MemoryRepository implementation for a memory-based repository.
        repo.repo_instance = MemoryRepository()
        #  Populate the memory repository with data from the provided from games.csv
        repo.repo_instance.populate()


    with app.app_context():
        from .browse import browse
        app.register_blueprint(browse.browse_blueprint)

        from .game import game
        app.register_blueprint(game.game_blueprint)

        from .search import search
        app.register_blueprint(search.search_blueprint)

        from .home import home
        app.register_blueprint(home.home_blueprint)

        from .authentication import authentication
        app.register_blueprint(authentication.authentication_blueprint)

        from .favourites import favourites
        app.register_blueprint(favourites.favourites_blueprint)

        from .wishlist import wishlist
        app.register_blueprint(wishlist.wishlist_blueprint)
        
        from .profile import profile
        app.register_blueprint(profile.profile_blueprint)
        
        @app.before_request
        def before_flask_http_request_function():
            if isinstance(repo.repo_instance, SqlAlchemyRepository):
                repo.repo_instance.reset_session()
                
        @app.teardown_appcontext
        def shutdown_session(exception=None):
            if isinstance(repo.repo_instance, SqlAlchemyRepository):
                repo.repo_instance.close_session()
    
    return app
