from flask import Blueprint, render_template, request, redirect, url_for, session, abort
import games.adapters.repository as repo
import games.search.services as services
from games.browse.browse import browse_games

search_blueprint = Blueprint('search_bp', __name__)


@search_blueprint.route('/search', methods=['GET'])
def search():
    query = request.args.get('query')
    category = request.args.get('category')  # get information from search url
    if query == "":
        return redirect(url_for('browse_bp.browse_all_games'))
    try:
        result = services.search_result(repo.repo_instance, query, category)
    except ValueError:
        abort(404)
        
    return browse_games(result, 'search_page.html', page=1)

