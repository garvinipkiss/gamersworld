import urllib.request,json
from .models import game



# Getting api key
api_key = None

# Getting the game base url
base_url = None

def configure_request(app):
    global api_key,base_url
    api_key = app.config['GAME_API_KEY']
    base_url = app.config['GAME_API_BASE_URL']






def get_games(category):
    '''
    Function that gets the json responce to our url request
    '''
    get_games_url = base_url.format(category,api_key)

    with urllib.request.urlopen(get_games_url) as url:
        get_games_data = url.read()
        get_games_response = json.loads(get_games_data)

        game_results = None

        if get_games_response['results']:
            game_results_list = get_games_response['results']
            game_results = process_results(game_results_list)


    return game_results


def get_game(id):
    get_game_details_url = base_url.format(id,api_key)

    with urllib.request.urlopen(get_game_details_url) as url:
        game_details_data = url.read()
        game_details_response = json.loads(game_details_data)

        game_object = None
        if game_details_response:
            id = game_details_response.get('id')
            title = game_details_response.get('original_title')
            overview = game_details_response.get('overview')
            poster = game_details_response.get('poster_path')
            vote_average = game_details_response.get('vote_average')
            vote_count = game_details_response.get('vote_count')

            game_object = game(id,title,overview,poster,vote_average,vote_count)

    return game_object



def search_game(game_name):
    search_movie_url = 'https://www.igdb.com/api/search/game?api_key={}&query={}'.format(api_key,movie_name)
    with urllib.request.urlopen(search_game_url) as url:
        search_game_data = url.read()
        search_game_response = json.loads(search_game_data)

        search_game_results = None

        if search_game_response['results']:
            search_game_list = search_game_response['results']
            search_game_results = process_results(search_game_list)


    return search_game_results




def process_results(game_list):
    '''
    Function  that processes the game result and transform them to a list of Objects

    Args:
        game_list: A list of dictionaries that contain game details

    Returns :
        game_results: A list of game objects
    '''
    game_results = []
    for game_item in game_list:
        id = game_item.get('id')
        title = game_item.get('original_title')
        overview = game_item.get('overview')
        poster = game_item.get('poster_path')
        vote_average = game_item.get('vote_average')
        vote_count = game_item.get('vote_count')

        if poster:

            game_object = game(id,title,overview,poster,vote_average,vote_count)
            game_results.append(game_object)

    return game_results
