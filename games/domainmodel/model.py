from datetime import datetime

class Screenshot:
    def __init__(self, link, game):
        self.link = link
        self.game = game
        
    @property
    def link(self):
        return self.__link
    
    @link.setter
    def link(self, new_link: str):
        if isinstance(new_link, str):
            self.__link = new_link
        else:
            self.__link = None
            
    @property
    def game(self):
        return self.__game
    
    @game.setter
    def game(self, new_game):
        if isinstance(new_game, Game):
            self.__game = new_game
        else:
            self.__game = None 


class Trailer:
    def __init__(self, link, game):
        self.link = link
        self.game = game

        
    @property
    def link(self):
        return self.__link
    
    @link.setter
    def link(self, new_link: str):
        if isinstance(new_link, str):
            self.__link = new_link
        else:
            self.__link = None
            
    @property
    def game(self):
        return self.__game
    
    @game.setter
    def game(self, new_game):
        if isinstance(new_game, Game):
            self.__game = new_game
        else:
            self.__game = None

class Publisher:
    def __init__(self, publisher_name: str):
        if publisher_name == "" or type(publisher_name) is not str:
            self.__publisher_name = None
        else:
            self.__publisher_name = publisher_name.strip()

    @property
    def publisher_name(self) -> str:
        return self.__publisher_name

    @publisher_name.setter
    def publisher_name(self, new_publisher_name: str):
        if new_publisher_name == "" or type(new_publisher_name) is not str:
            self.__publisher_name = None
        else:
            self.__publisher_name = new_publisher_name.strip()

    def __repr__(self):
        return f'<Publisher {self.__publisher_name}>'

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return False
        return other.publisher_name == self.__publisher_name

    def __lt__(self, other):
        if not isinstance(other, self.__class__):
            return False
        return self.__publisher_name < other.publisher_name

    def __hash__(self):
        return hash(self.__publisher_name)


class Developer:
    def __init__(self, developer_name: str):
        if developer_name == "" or type(developer_name) is not str:
            self.__developer_name = None
        else:
            self.__developer_name = developer_name.strip()

    @property
    def developer_name(self) -> str:
        return self.__developer_name

    @developer_name.setter
    def developer_name(self, new_developer_name: str):
        if new_developer_name == "" or type(new_developer_name) is not str:
            self.__developer_name = None
        else:
            self.__developer_name = new_developer_name.strip()

    def __repr__(self):
        return f'<Developer {self.__developer_name}>'

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return False
        return other.developer_name == self.__developer_name

    def __lt__(self, other):
        if isinstance(other, self.__class__):
            return self.__developer_name < other.developer_name
        return False

    def __hash__(self):
        return hash(self.__developer_name)


class Genre:
    def __init__(self, genre_name: str):
        if genre_name == "" or type(genre_name) is not str:
            self.__genre_name = None
        else:
            self.__genre_name = genre_name.strip()

    @property
    def genre_name(self) -> str:
        return self.__genre_name

    def __repr__(self) -> str:
        return f'<Genre {self.__genre_name}>'

    def __eq__(self, other) -> bool:
        if not isinstance(other, self.__class__):
            return False
        return other.genre_name == self.__genre_name

    def __lt__(self, other):
        if not isinstance(other, self.__class__):
            return False
        return self.__genre_name < other.genre_name

    def __hash__(self):
        return hash(self.__genre_name)
    
    
"""class Category:
    def __init__(self, category_name: str):
        if category_name == "" or type(category_name) is not str:
            self.__category_name = None
        else:
            self.__category_name = category_name.strip()

    @property
    def category_name(self) -> str:
        return self.__category_name

    def __repr__(self) -> str:
        return f'<Genre {self.__category_name}>'

    def __eq__(self, other) -> bool:
        if not isinstance(other, self.__class__):
            return False
        return other.category_name == self.__category_name

    def __lt__(self, other):
        if not isinstance(other, self.__class__):
            return False
        return self.__category_name < other.category_name

    def __hash__(self):
        return hash(self.__category_name)
"""

class Game:
    def __init__(self, game_id: int, game_title: str):
        if type(game_id) is not int or game_id < 0:
            raise ValueError("Game ID should be a positive integer!")
        self.__game_id = game_id

        if type(game_title) is str and game_title.strip() != "":
            self.__game_title = game_title.strip()
        else:
            self.__game_title = None

        self.__price = None
        self.__release_date = None
        self.__description = None
        self.__image_url = None
        self.__website_url = None
        self.__genres: list = []
        self.__categories: list = []
        self.__reviews: list = []
        self.__publisher = None
        self.__developer = None
        self.__achievements = None
        self.__recommendations = None
        self.__screenshots: list = []
        self.__trailers: list = []
        self.__notes = None
        self.__windows = None
        self.__apple = None
        self.__linux = None
        self.__average_rating = 0
        
        
    #probably in the wrong place   
    #temporary 
    @property
    def average_rating(self) -> float:
        return self.__average_rating
    
    @property
    def review_text(self) -> str:
        return self.__review_text
    
    
    @review_text.setter
    def review_text(self, review_text: str):
        if isinstance(review_text, str):
            self.__review_text = review_text
        else:
            self.__review_text = None 
    
    #temporary
    
    
    """@property
    def categories(self) -> list:
        return self.__categories

    def add_category(self, category: Category):
        if not isinstance(category, Category) or category in self.__categories:
            return
        self.__categories.append(category)

    def remove_category(self, category: Category):
        if not isinstance(category, Category):
            return
        try:
            self.__categories.remove(category)
        except ValueError:
            print(f"Could not find {category} in list of categories.")
            pass"""

    
    @property
    def windows(self) -> bool:
        return self.__windows
    
    @windows.setter
    def windows(self, windows: bool):
        if isinstance(windows, bool):
            self.__windows = windows
        else:
            self.__windows = None
            
    @property
    def apple(self) -> bool:
        return self.__apple
    
    @apple.setter
    def apple(self, apple: bool):
        if isinstance(apple, bool):
            self.__apple = apple
        else:
            self.__apple = None
            
    @property
    def linux(self) -> bool:
        return self.__linux
    
    @linux.setter
    def linux(self, linux: bool):
        if isinstance(linux, bool):
            self.__linux = linux
        else:
            self.__linux = None
            
    #end of probably in the wrong place.    
            
            
            
    @property
    def publisher(self) -> Publisher:
        return self.__publisher

    @publisher.setter
    def publisher(self, publisher: Publisher):
        if isinstance(publisher, Publisher):
            self.__publisher = publisher
        else:
            self.__publisher = None

    @property
    def developer(self) -> Developer:
        return self.__developer

    @developer.setter
    def developer(self, developer: Developer):
        if isinstance(developer, Developer):
            self.__developer = developer
        else:
            self.__developer = None

    @property
    def game_id(self):
        return self.__game_id

    @property
    def title(self):
        return self.__game_title

    @title.setter
    def title(self, new_title):
        if type(new_title) is str and new_title.strip() != "":
            self.__game_title = new_title.strip()
        else:
            self.__game_title = None

    @property
    def price(self):
        return self.__price

    @price.setter
    def price(self, price: float):
        if isinstance(price, (int, float)) and price >= 0:
            self.__price = price
        else:
            raise ValueError("Price must be a positive number!")

    @property
    def achievements(self):
        return self.__achievements

    @achievements.setter
    def achievements(self, achievements: int):
        if isinstance(achievements, int) and achievements >= 0:
            self.__achievements = achievements
        else:
            raise ValueError("Number of achievements must be a positive number")

    @property
    def recommendations(self):
        return self.__recommendations

    @recommendations.setter
    def recommendations(self, recommendations: int):
        if isinstance(recommendations, int) and recommendations >= 0:
            self.__recommendations = recommendations
        else:
            raise ValueError("Number of recommendations must be a positive number")

    @property
    def release_date(self):
        return self.__release_date

    @release_date.setter
    def release_date(self, release_date: str):
        if isinstance(release_date, str):
            try:
                # Check if the release_date string is in the correct date format (e.g., "Oct 21, 2008")
                datetime.strptime(release_date, "%b %d, %Y")
                self.__release_date = release_date
            except ValueError:
                raise ValueError("Release date must be in 'Oct 21, 2008' format!")
        else:
            raise ValueError("Release date must be a string in 'Oct 21, 2008' format!")

    @property
    def description(self):
        return self.__description

    @description.setter
    def description(self, description: str):
        if isinstance(description, str) and description.strip() != "":
            self.__description = description
        else:
            self.__description = None

    @property
    def image_url(self):
        return self.__image_url

    @image_url.setter
    def image_url(self, image_url: str):
        if isinstance(image_url, str) and image_url.strip() != "":
            self.__image_url = image_url
        else:
            self.__image_url = None

    @property
    def website_url(self):
        return self.__website_url

    @website_url.setter
    def website_url(self, website_url: str):
        if isinstance(website_url, str) and website_url.strip() != "":
            self.__website_url = website_url
        else:
            self.__website_url = None

    @property
    def reviews(self) -> list:
        return self.__reviews
    

    def add_review(self, review):
        if isinstance(review, Review):
            if review not in self.reviews:
                self.__reviews.append(review)
                
                        
    def remove_review(self, review):
        if isinstance(review, Review):
            if review in self.reviews:
                self.decrease_average_rating(review.rating, review.user)
                self.__reviews.remove(review)
                
                
    def increase_average_rating(self, user, rating):
        users = [review.user for review in self.__reviews]
        if user in users:
            return
        self.__average_rating = (self.__average_rating * len(self.reviews) + rating) / (len(self.reviews) + 1)
        
        
    def decrease_average_rating(self, user, rating):
        users = [review.user for review in self.__reviews]
        if user in users:
            return
        self.__average_rating = (self.__average_rating * len(self.reviews) - rating) / (len(self.reviews) - 1)

    @property
    def genres(self) -> list:
        return self.__genres

    def add_genre(self, genre: Genre):
        if not isinstance(genre, Genre) or genre in self.__genres:
            return
        self.__genres.append(genre)

    def remove_genre(self, genre: Genre):
        if not isinstance(genre, Genre):
            return
        try:
            self.__genres.remove(genre)
        except ValueError:
            print(f"Could not find {genre} in list of genres.")
            pass

    @property
    def screenshots(self):
        return self.__screenshots

    def add_screenshot(self, screenshot: Screenshot):
        if not isinstance(screenshot, Screenshot) or screenshot in self.__screenshots:
            return
        self.__screenshots.append(screenshot)

    def remove_screenshot(self, screenshot: Screenshot):
        if not isinstance(screenshot, Screenshot):
            return
        try:
            self.__screenshots.remove(screenshot)
        except ValueError:
            print("That screenshot is not in the list of screenshots")
            pass

    @property
    def trailers(self):
        return self.__trailers

    def add_trailer(self, trailer: Trailer):
        if not isinstance(trailer, Trailer) or trailer in self.__trailers:
            return
        self.__trailers.append(trailer)

    def remove_trailer(self, trailer: Trailer):
        if not isinstance(trailer, Trailer):
            return
        try:
            self.__trailers.remove(trailer)
        except ValueError:
            print("This trailer is not in the list of trailers")
            pass

    @property
    def notes(self):
        return self.__notes

    @notes.setter
    def notes(self, note: str):
        if isinstance(note, str) and note.strip() != "":
            self.__notes = note
        else:
            self.__notes = None

    def __repr__(self):
        return f"<Game {self.__game_id}, {self.__game_title}>"

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return False
        return self.__game_id == other.__game_id

    def __hash__(self):
        return hash(self.__game_id)

    def __lt__(self, other):
        if not isinstance(other, self.__class__):
            return False
        return self.__game_id < other.game_id


class User:
    def __init__(self, username: str, password: str):
        if not isinstance(username, str) or username.strip() == "":
            raise ValueError('Username cannot be empty or non-string!')
        else:
            self.__username = username.lower().strip()

        if isinstance(password, str) and len(password) >= 7:
            self.__password = password
        else:
            raise ValueError('Password not valid!')

        self.__reviews: list[Review] = []
        self.__favourite_games: Favourites = Favourites(self)
        self.__wishlist: Wishlist = Wishlist(self)
        self.__profile: Profile = Profile()
        
    @property
    def profile(self):
        return self.__profile

    @profile.setter
    def profile(self, new_prof):
        if isinstance(new_prof, Profile):
            self.__profile = new_prof

    @property
    def username(self):
        return self.__username

    @property
    def password(self) -> str:
        return self.__password

    @property
    def reviews(self) -> list:
        return self.__reviews

    def add_review(self, new_review):
        if not isinstance(new_review, Review) or new_review in self.reviews:
            return
        self.__reviews.append(new_review)

    def remove_review(self, review):
        if not isinstance(review, Review) or review not in self.__reviews:
            return
        self.__reviews.remove(review)

    @property
    def favourite_games(self):
        return self.__favourite_games

    def add_favourite_game(self, game):
        if not isinstance(game, Game) or self.favourite_games.contains(game):
            return
        self.favourite_games.add_game(game)

    def remove_favourite_game(self, game):
        if not isinstance(game, Game) or not self.favourite_games.contains(game):
            return
        self.favourite_games.remove_game(game)

    @property
    def wishlist(self):
        return self.__wishlist

    def add_to_wishlist(self, game: Game):
        if isinstance(game, Game) and not self.wishlist.contains(game):
            self.__wishlist.add_game(game)

    def remove_from_wishlist(self, game: Game):
        if isinstance(game, Game) and self.wishlist.contains(game):
            self.__wishlist.remove_game(game)

    def size_of_wishlist(self):
        self.wishlist.size

    def first_game_in_wishlist(self):
        return self.wishlist.first_game_in_list()

    def select_game_from_wishlist(self, index):
        return self.wishlist.select_game(index)

    #  __iter__ and __next__ from Wishlist class is not yet implemented

    def __repr__(self):
        return f"<User {self.__username}>"

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return False
        return self.__username == other.username

    def __hash__(self):
        return hash(self.__username)

    def __lt__(self, other):
        if not isinstance(other, self.__class__):
            return False
        return self.__username < other.username
    
    

class Review:
    def __init__(self, user: User, game: Game, rating: int, comment: str):
        
        self.comment = comment
        self.rating = rating
        game.increase_average_rating(user, rating)
        self.user = user
        self.game = game
        
        game.add_review(self)
        user.add_review(self)
        

    @property
    def game(self) -> Game:
        return self.__game

    @property
    def comment(self) -> str:
        return self.__comment

    @property
    def rating(self) -> int:
        return self.__rating

    @property
    def user(self) -> User:
        return self.__user
    
    @user.setter
    def user(self, new_user):
        if isinstance(new_user, User):
            self.__user = new_user
        else:
            print("user was not set")
            raise ValueError("User must be a user")
            
    @game.setter
    def game(self, new_game):
        if isinstance(new_game, Game):
            self.__game = new_game
        else:
            print("game was not set")
            raise ValueError("Game must be a game")

    @comment.setter
    def comment(self, new_text):
        if isinstance(new_text, str):
            self.__comment = new_text.strip()
        else:
            raise ValueError("New comment must be a string")

    @rating.setter
    def rating(self, new_rating: int):
        if isinstance(new_rating, int) and 0 <= new_rating <= 5:
            self.__rating = new_rating
        else:
            raise ValueError("Rating must be an integer between 0 and 5")

    def __repr__(self):
        return f"Review(User: {self.__user}, Game: {self.__game}, " \
               f"Rating: {self.__rating}, Comment: {self.__comment})"

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return False
        return other.user == self.__user and other.game == self.__game
    
    def __hash__(self):
        return hash(str(self.game) + str(self.user))


class Wishlist:
    def __init__(self, user: User):
        if not isinstance(user, User):
            raise ValueError("User must be an instance of User class")
        self.__user = user
        self.__list_of_games = []
        
    @property
    def user(self):
        return self.__user

    @property
    def list_of_games(self):
        return self.__list_of_games

    def size(self):
        size_wishlist = len(self.__list_of_games)
        if size_wishlist > 0:
            return size_wishlist

    def add_game(self, game: Game):
        if isinstance(game, Game) and game not in self.__list_of_games:
            self.__list_of_games.append(game)

    def first_game_in_list(self):
        if len(self.__list_of_games) > 0:
            return self.__list_of_games[0]
        else:
            return None

    def remove_game(self, game):
        if isinstance(game, Game) and game in self.__list_of_games:
            self.__list_of_games.remove(game)

    def select_game(self, index):
        if 0 <= index < len(self.__list_of_games):
            return self.__list_of_games[index]
        else:
            return None
        
    def contains(self, game: Game) -> bool:
        return game in self.list_of_games

    def __iter__(self):
        self.__current = 0
        return self

    def __next__(self):
        if self.__current >= len(self.__list_of_games):
            raise StopIteration
        else:
            self.__current += 1
            return self.__list_of_games[self.__current - 1]
        
    def __len__(self):
        return len(self.list_of_games)
    
    def __repr__(self):
        return str(self.list_of_games)



class Favourites:
    def __init__(self, user: User):
        if not isinstance(user, User):
            raise ValueError("User must be an instance of User class")
        self.__user = user
        self.__list_of_games = []

        
    @property
    def user(self):
        return self.__user

      
    @property
    def list_of_games(self):
        return self.__list_of_games

      
    def size(self):
        size_favourites = len(self.__list_of_games)
        if size_favourites > 0:
            return size_favourites

          
    def add_game(self, game: Game):
        if isinstance(game, Game) and game not in self.__list_of_games:
            self.__list_of_games.append(game)

            
    def first_game_in_list(self):
        if len(self.__list_of_games) > 0:
            return self.__list_of_games[0]
        else:
            return None

          
    def remove_game(self, game):
        if isinstance(game, Game) and game in self.__list_of_games:
            self.__list_of_games.remove(game)

            
    def select_game(self, index):
        if 0 <= index < len(self.__list_of_games):
            return self.__list_of_games[index]
        else:
            return None

          
    def contains(self, game: Game) -> bool:
        return game in self.list_of_games

      
    def __iter__(self):
        self.__current = 0
        return self

      
    def __next__(self):
        if self.__current >= len(self.__list_of_games):
            raise StopIteration
        else:
            self.__current += 1
            return self.__list_of_games[self.__current - 1]

          
    def __len__(self):
        return len(self.list_of_games)

    def __repr__(self):
        return str(self.list_of_games)

        

class Profile:
    def __init__(self):
        self.__description = "Hi new user, to update the homepage, you can click the settings button. In there, you can change your description, choose whether to show your favourite games, your wishlist and your comments."
        self.__show_favourites = True
        self.__show_wishlist = True
        self.__show_comments = True 
        
        
    @property
    def description(self):
        return self.__description
    
    
    @description.setter
    def description(self, new_desc):
        if isinstance(new_desc, str):
            self.__description = new_desc
        
        
    @property        
    def show_favourites(self):
        return self.__show_favourites
    
    
    @show_favourites.setter
    def show_favourites(self, show_fav):
        if isinstance(show_fav, bool):
            self.__show_favourites = show_fav
      
      
    @property        
    def show_wishlist(self):
        return self.__show_wishlist
    
    
    @show_wishlist.setter
    def show_wishlist(self, show_wish):
        if isinstance(show_wish, bool):
            self.__show_wishlist = show_wish
     
    
    @property        
    def show_comments(self):
        return self.__show_comments
    
    
    @show_comments.setter
    def show_comments(self, show_comm):
        if isinstance(show_comm, bool):
            self.__show_comments = show_comm
        
        