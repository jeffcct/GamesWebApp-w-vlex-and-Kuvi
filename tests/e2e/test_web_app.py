import pytest
import os
from flask import url_for, session, request
from games.home.home import home_blueprint


def test_home_route(client):
    #  test route for home page
    response = client.get('/')
    assert response.status_code == 200
    assert b"Welcome to our Games Library app!" in response.data


def test_browse_route(client):
    #  test route for browsing all games
    response = client.get('/games')
    assert response.status_code == 308
    assert b"Redirecting" in response.data


def test_browse_genre_route(client):
    #  check each genre in the genre sidebar if each genre returns games
    response = client.get('/games/Action')
    assert response.status_code == 200
    assert b"Modern Warfare" in response.data

    response = client.get('/games/Adventure')
    assert response.status_code == 200
    assert b"Deadfall Adventures" in response.data

    response = client.get('/games/Animation%20&%20Modeling')
    assert response.status_code == 200
    assert b"Dough" in response.data

    response = client.get('/games/Audio%20Production')
    assert response.status_code == 200
    assert b"Avalive" in response.data

    response = client.get('/games/Casual')
    assert response.status_code == 200
    assert b"Tidalis" in response.data

    response = client.get('/games/Design%20&%20Illustration')
    assert response.status_code == 200
    assert b"XWallpaper" in response.data

    response = client.get('/games/Early%20Access')
    assert response.status_code == 200
    assert b"Ymir" in response.data

    response = client.get('/games/Education')
    assert response.status_code == 200
    assert b"Kooring VR Coding Adventure" in response.data

    response = client.get('/games/Free%20to%20Play')
    assert response.status_code == 200
    assert b"HIT" in response.data

    response = client.get('/games/Game%20Development')
    assert response.status_code == 200
    assert b"AvatarShop" in response.data

    response = client.get('/games/Gore')
    assert response.status_code == 200
    assert b"Russian Gangsta In HELL" in response.data

    response = client.get('/games/Indie')
    assert response.status_code == 200
    assert b"Fowl Space" in response.data

    response = client.get('/games/Massively%20Multiplayer')
    assert response.status_code == 200
    assert b"Rogalia" in response.data

    response = client.get('/games/Photo%20Editing')
    assert response.status_code == 200
    assert b"RGByte" in response.data

    response = client.get('/games/RPG')
    assert response.status_code == 200
    assert b"Desktop Dungeons" in response.data

    response = client.get('/games/Racing')
    assert response.status_code == 200
    assert b"Hare" in response.data

    response = client.get('/games/Simulation')
    assert response.status_code == 200
    assert b"Fish Tycoon" in response.data

    response = client.get('/games/Software%20Training')
    assert response.status_code == 200
    assert b"Mavis Beacon Teaches Typing Family Edition" in response.data

    response = client.get('/games/Sports')
    assert response.status_code == 200
    assert b"Gunball" in response.data

    response = client.get('/games/Strategy')
    assert response.status_code == 200
    assert b"Tenshu General" in response.data

    response = client.get('/games/Utilities')
    assert response.status_code == 200
    assert b"Borderless Gaming" in response.data

    response = client.get('/games/Video%20Production')
    assert response.status_code == 200
    assert b"VSS - Virtual Streaming Software" in response.data

    response = client.get('/games/Violent')
    assert response.status_code == 200
    assert b"CrisisActionVR" in response.data

    response = client.get('/games/Web%20Publishing')
    assert response.status_code == 200
    assert b"Piecewise: build chat bots with blocks" in response.data


def test_game_description_route(client):
    #  check if game description page shows up for a game
    response = client.get('/game/40800')
    assert response.status_code == 200
    assert b"Super Meat Boy" in response.data

    response = client.get('/game/1172470')
    assert response.status_code == 200
    assert b"Conquer with character in Apex Legends" in response.data


def test_browse_pagination(client):
    #  check if pagination is working
    response = client.get('/games/?page=2')
    assert response.status_code == 200

    #  check if last page is working
    response = client.get('/games/?page=18')
    assert response.status_code == 200


def test_search_results(client):
    response = client.get('/search?query=xpand&category=Name')              # test searching by Name
    assert response.status_code == 200
    assert b"Xpand Rally" in response.data

    response = client.get('/search?query=racing&category=Genre')            # test searching by Name
    assert response.status_code == 200
    assert b"Forza Horizon 4" in response.data

    response = client.get('/search?query=bandai&category=Publisher')        # test searching by Name
    assert response.status_code == 200
    assert b"MUD Motocross World Championship" in response.data
    assert b"Hexodius" in response.data


# def test_register(client):
#     # Check that we retrieve the register page.
#     response_code = client.get('/register').status_code
#     assert response_code == 200
#
#     # Check that we can register a user successfully, supplying a valid user name and password.
#     response = client.post(
#         '/register',
#         data={'user_name': 'gmichael', 'password': 'CarelessWhisper1984'},
#      follow_redirects = True
#     )
#     assert response.headers['Location'] == '/login'
#

@pytest.mark.parametrize(('user_name', 'password', 'message'), (
        ('', '', b'Your user name is required'),
        ('cj', '', b'Your user name is too short'),
        ('test', '', b'Your password is required'),
        ('test', 'test', b'haracters long, have an uppercase, lowercase and a digit'),
))
def test_register_with_invalid_input(client, user_name, password, message):
    # Check that attempting to register with invalid combinations of user name and password generate appropriate error
    # messages.
    response = client.post(
        '/register',
        data={'user_name': user_name, 'password': password}
    )
    assert message in response.data



def test_login(client, auth):
    status_code = client.get('/login').status_code
    assert status_code == 200

    response = auth.login()

    with client:
        response = auth.login()
        client.get('/')
        # assert session['user_name'] == 1
        assert response.status_code == 200


# def test_login_again(client, auth):
#     response = client.get('/')
#     assert b'Register' in response.data
#
#     response = auth.login()
#     assert session.get('user_name') == 'test'
#     # assert b'Profile' in response.data
#
#     # home_response = client.get(login_response.headers['Location'])
#     # assert b'Profile' in home_response.data
#
#     # with client.session_transaction() as session:
#         # session['user_name'] = 'testuser'
#
#     # response = client.get('profile/testuser')
#     # assert b'Profile' in response.data



"""
def test_wishlist_page(client, auth):
    auth.login()

    response = client.get('/wishlist')
    assert response.status_code == 302
    assert b"Wishlisted Games"


def test_favourites_page(client, auth):
    auth.login()

    response = client.get('/favourites')
    assert response.status_code == 302
    assert b"Favourites"

"""

def test_register(new_client):
    response = new_client.post("/register", data={
        'user_name': 'gmichael',
        'password': 'CarelessWhisper1984'

    },follow_redirects=True)
    assert response.status_code == 200
    assert response.request.path == "/login"
    assert len(response.history) == 1

def test_new_login(new_client):
    response = new_client.post("/register", data={
        'user_name': 'gmichael',
        'password': 'CarelessWhisper1984'

    }, follow_redirects=True)
    new_response = new_client.post("/login", data={
        'user_name': 'gmichael',
        'password': 'CarelessWhisper1984'

    }, follow_redirects=True)
    assert new_response.request.path == "/"
    with new_client:
        new_client.get("/")
        assert session['user_name'] == 'gmichael'


def test_wishlist(new_client):
    response = new_client.post("/register", data={
        'user_name': 'gmichael',
        'password': 'CarelessWhisper1984'

    }, follow_redirects=True)
    new_response = new_client.post("/login", data={
        'user_name': 'gmichael',
        'password': 'CarelessWhisper1984'

    }, follow_redirects=True)
    assert new_response.request.path == "/"
    with new_client:
        response = new_client.get("/wishlist")
        assert session['user_name'] == 'gmichael'
        assert response.status_code == 200
        assert b'Wishlisted Games' in response.data

def test_favourites(new_client):
    response = new_client.post("/register", data={
        'user_name': 'gmichael',
        'password': 'CarelessWhisper1984'

    }, follow_redirects=True)
    new_response = new_client.post("/login", data={
        'user_name': 'gmichael',
        'password': 'CarelessWhisper1984'

    }, follow_redirects=True)
    assert new_response.request.path == "/"
    with new_client:
        response = new_client.get("/favourites")
        assert session['user_name'] == 'gmichael'
        assert response.status_code == 200
        assert b'Favourites' in response.data
