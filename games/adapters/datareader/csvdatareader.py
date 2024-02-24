import csv
import os

from games.domainmodel.model import Genre, Game, Publisher, Developer, Trailer, Screenshot


class GameFileCSVReader:
    def __init__(self, filename):
        self.__filename = filename
        self.__dataset_of_games = []
        self.__dataset_of_publishers = set()
        self.__dataset_of_genres = set()
        self.__dataset_of_developers = set()
        self.__dataset_of_categories = set()
        self.__dataset_of_screenshots = set()
        self.__dataset_of_trailers = set()

    def read_csv_file(self):
        if not os.path.exists(self.__filename):
            print(f"path {self.__filename} does not exist!")
            return
        with open(self.__filename, 'r', encoding='utf-8-sig') as file:
            reader = csv.DictReader(file)
            for row in reader:
                try:
                    game_id = int(row["AppID"])
                    title = row["Name"]
                    game = Game(game_id, title)
                    #
                    game.review_text = row["Reviews"]
                    #
                    game.release_date = row["Release date"]
                    game.price = float(row["Price"])
                    game.description = row["About the game"]
                    game.image_url = row["Header image"]
                    game.website_url = row["Website"]
                    publisher = Publisher(row["Publishers"])
                    self.__dataset_of_publishers.add(publisher)
                    game.publisher = publisher
                    developer = Developer(row["Developers"])
                    self.__dataset_of_developers.add(developer)
                    game.developer = developer
                    game.recommendations = int(row["Recommendations"])
                    game.achievements = int(row["Achievements"])
                    game.notes = row["Notes"]
                    game.windows = True if row["Windows"] == "TRUE" else False
                    game.linux = True if row["Linux"] == "TRUE" else False
                    game.apple = True if row["Mac"] == "TRUE" else False
                    

                    genre_names = row["Genres"].split(",")
                    for genre_name in genre_names:
                        genre = Genre(genre_name.strip())
                        self.__dataset_of_genres.add(genre)
                        game.add_genre(genre)
                        
                    """category_names = row["Categories"].split(",")
                    for category_name in category_names:
                        category = Category(category_name.strip())
                        game.add_category(category)
                        self.__dataset_of_categories.add(category)"""

                    screenshots = row["Screenshots"].split(",")
                    for screenshot in screenshots:
                        if screenshot == '':
                            continue
                        screenshot = Screenshot(screenshot, game)
                        game.add_screenshot(screenshot)
                        self.__dataset_of_screenshots.add(screenshot)

                    trailers = row["Movies"].split(",")
                    for trailer in trailers:
                        if trailer == '':
                            continue
                        trailer = Trailer(trailer, game)
                        game.add_trailer(trailer)
                        self.__dataset_of_trailers.add(trailer)

                    self.__dataset_of_games.append(game)

                except ValueError as e:
                    print(f"Skipping row due to invalid data: {e}")
                except KeyError as e:
                    print(f"Skipping row due to missing key: {e}")

    def get_unique_games_count(self):
        return len(self.__dataset_of_games)

    def get_unique_genres_count(self):
        return len(self.__dataset_of_genres)

    def get_unique_publishers_count(self):
        return len(self.__dataset_of_publishers)

    @property
    def dataset_of_games(self) -> list:
        return self.__dataset_of_games

    @property
    def dataset_of_publishers(self) -> set:
        return self.__dataset_of_publishers

    @property
    def dataset_of_genres(self) -> set:
        return self.__dataset_of_genres

    @property
    def dataset_of_developers(self) -> set:
        return self.__dataset_of_developers
    
    @property
    def dataset_of_categories(self) -> set:
        return self.__dataset_of_categories
    
    @property
    def dataset_of_trailers(self) -> set:
        return self.__dataset_of_trailers
    
    @property
    def dataset_of_screenshots(self) -> set:
        return self.__dataset_of_screenshots
