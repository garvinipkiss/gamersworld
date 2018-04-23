from flask import render_template,request,redirect,url_for,abort
from . import main
from ..requests import get_games,get_game,search_game
from .forms import ReviewForm,UpdateProfile
from ..models import Review,User,PhotoProfile
from flask_login import login_required,current_user
from .. import db,photos

import markdown2


# Views
@main.route('/')
def index():

    '''
    View root page function that returns the index page and its data
    '''

    # Getting popular game
    popular_games = get_games('popular')
    upcoming_game = get_games('upcoming')
    now_playing_game = get_games('now_playing')

    title = 'Home - Welcome to The best game Review Website Online'

    search_game = request.args.get('game_query')

    if search_game:
        return redirect(url_for('.search',game_name=search_game))
    else:
        return render_template('index.html', title = title, popular = popular_games, upcoming = upcoming_game, now_playing = now_playing_game )


@main.route('/game/<int:id>')
def movie(id):

    '''
    View game page function that returns the game details page and its data
    '''
    game = get_game(id)
    title = f'{game.title}'
    reviews = Review.get_reviews(game.id)

    return render_template('game.html',title = title,game = game,reviews = reviews)



@main.route('/search/<game_name>')
def search(game_name):
    '''
    View function to display the search results
    '''
    game_name_list = game_name.split(" ")
    game_name_format = "+".join(game_name_list)
    searched_games = search_game(game_name_format)
    title = f'search results for {game_name}'
    return render_template('search.html',games = searched_games)


@main.route('/reviews/<int:id>')
def game_reviews(id):
    game = get_game(id)

    reviews = Review.get_reviews(id)
    title = f'All reviews for {game.title}'
    return render_template('game_reviews.html',title = title,reviews=reviews)


@main.route('/review/<int:id>')
def single_review(id):
    review=Review.query.get(id)
    format_review = markdown2.markdown(review.movie_review,extras=["code-friendly", "fenced-code-blocks"])
    return render_template('review.html',review = review,format_review=format_review)




@main.route('/game/review/new/<int:id>', methods = ['GET','POST'])
@login_required
def new_review(id):

    form = ReviewForm()

    game = get_game(id)

    if form.validate_on_submit():
        title = form.title.data
        review = form.review.data

        new_review = Review(game_id=game.id,game_title=title,image_path=game.poster,game_review=review,user=current_user)

        new_review.save_review()

        return redirect(url_for('.game',id = game.id ))

    title = f'{movie.title} review'
    return render_template('new_review.html',title = title, review_form=form, movie=movie)

@main.route('/user/<uname>')

def profile(uname):
    user = User.query.filter_by(username = uname).first()

    if user is None:
        abort(404)

    return render_template("profile/profile.html", user = user)


@main.route('/user/<uname>/update',methods = ['GET','POST'])
@login_required
def update_profile(uname):
    user = User.query.filter_by(username = uname).first()
    if user is None:
        abort(404)

    form = UpdateProfile()

    if form.validate_on_submit():

        user.bio = form.bio.data

        db.session.add(user)
        db.session.commit()

        return redirect(url_for('.profile',uname=user.username))

    return render_template('profile/update.html',form =form)


@main.route('/user/<uname>/update/pic',methods= ['POST'])
@login_required
def update_pic(uname):
    user = User.query.filter_by(username = uname).first()
    if 'photo' in request.files:
        filename = photos.save(request.files['photo'])
        path = f'photos/{filename}'
        user.profile_pic_path = path
        user_photo = PhotoProfile(pic_path = path,user = user)
        db.session.commit()
    return redirect(url_for('main.profile',uname=uname))
