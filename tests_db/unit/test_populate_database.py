from sqlalchemy import select, inspect

from games.adapters.orm import metadata

def test_database_populate_inspect_table_names(database_engine):
    # Get table information
    inspector = inspect(database_engine)
    assert inspector.get_table_names() == ['developers',
                                           'favourites',
                                           'favourites_game_assoc',
                                           'games',
                                           'games_genre_assoc',
                                           'genres',
                                           'profile',
                                           'publishers',
                                           'reviews',
                                           'screenshot',
                                           'trailer',
                                           'users',
                                           'wishlist',
                                           'wishlist_game_assoc']


# test games table
def test_database_populate_select_games(database_engine):
    # Get table info
    inspector = inspect(database_engine)
    name_of_games_table = inspector.get_table_names()[3]

    with database_engine.connect() as connection:
        select_statement = select([metadata.tables[name_of_games_table]])
        result = connection.execute(select_statement)

        all_game_names = []
        for row in result:
            all_game_names.append(row['game_title'])

        assert all_game_names == ['Call of Duty® 4: Modern Warfare®', "Bartlow's Dread Machine"]



# test publishers table
def test_database_populate_select_publishers(database_engine):
    # Get table info
    inspector = inspect(database_engine)
    name_of_publishers_table = inspector.get_table_names()[7]

    with database_engine.connect() as connection:
        select_statement = select([metadata.tables[name_of_publishers_table]])
        result = connection.execute(select_statement)

        all_publisher_names = []
        for row in result:
            all_publisher_names.append(row['name'])

        assert all_publisher_names == ['Activision', 'Beep Games, Inc.']


# test developers table
def test_database_populate_select_developers(database_engine):
    # Get table info
    inspector = inspect(database_engine)
    name_of_developers_table = inspector.get_table_names()[0]

    with database_engine.connect() as connection:
        select_statement = select([metadata.tables[name_of_developers_table]])
        result = connection.execute(select_statement)

        all_developer_names = []
        for row in result:
            all_developer_names.append(row['name'])

        assert all_developer_names == ['Infinity Ward', 'Beep Games, Inc.,Tribetoy']


# genres table
def test_database_populate_select_genres(database_engine):
    # Get table info
    inspector = inspect(database_engine)
    name_of_genres_table = inspector.get_table_names()[5]

    with database_engine.connect() as connection:
        select_statement = select([metadata.tables[name_of_genres_table]])
        result = connection.execute(select_statement)

        all_genre_names = []
        for row in result:
            all_genre_names.append(row['name'])

        assert all_genre_names == ['Action']


# test screenshot table
def test_database_populate_select_screenshots(database_engine):
    # Get table info
    inspector = inspect(database_engine)
    name_of_screenshots_table = inspector.get_table_names()[9]

    with database_engine.connect() as connection:
        select_statement = select([metadata.tables[name_of_screenshots_table]])
        result = connection.execute(select_statement)

        all_screenshot_links = []
        for row in result:
            all_screenshot_links.append(row['link'])

        assert 'https://cdn.akamai.steamstatic.com/steam/apps/7940/0000002987.1920x1080.jpg?t=1646762118' in all_screenshot_links
        assert 'https://cdn.akamai.steamstatic.com/steam/apps/1228870/ss_a82a166144406f3ab26f931c5ffb3e865e83f5bd.1920x1080.jpg?t=1601679243' in all_screenshot_links
        assert len(all_screenshot_links) == 88


# test trailer table
def test_database_populate_select_trailers(database_engine):
    # Get table info
    inspector = inspect(database_engine)
    name_of_trailers_table = inspector.get_table_names()[10]

    with database_engine.connect() as connection:
        select_statement = select([metadata.tables[name_of_trailers_table]])
        result = connection.execute(select_statement)

        all_trailer_links = []
        for row in result:
            all_trailer_links.append(row['link'])

        assert 'http://cdn.akamai.steamstatic.com/steam/apps/256803408/movie_max.mp4?t=1601679223' in all_trailer_links


def test_database_populate_select_users(database_engine):
    # Get table info
    inspector = inspect(database_engine)
    name_of_users_table = inspector.get_table_names()[11]

    with database_engine.connect() as connection:
        select_statement = select([metadata.tables[name_of_users_table]])
        result = connection.execute(select_statement)

        all_users = []
        for row in result:
            all_users.append(row['username'])

        assert all_users == []


def test_database_populate_select_favourites(database_engine):
    # Get table info
    inspector = inspect(database_engine)
    name_of_favourites_table = inspector.get_table_names()[1]

    with database_engine.connect() as connection:
        select_statement = select([metadata.tables[name_of_favourites_table]])
        result = connection.execute(select_statement)

        all_favourites = []
        for row in result:
            all_favourites.append(row['id'])

        assert all_favourites == []


def test_database_populate_select_wishlist(database_engine):
    # Get table info
    inspector = inspect(database_engine)
    name_of_wishlist_table = inspector.get_table_names()[12]

    with database_engine.connect() as connection:
        select_statement = select([metadata.tables[name_of_wishlist_table]])
        result = connection.execute(select_statement)

        all_wishlist = []
        for row in result:
            all_wishlist.append(row['id'])

        assert all_wishlist == []
