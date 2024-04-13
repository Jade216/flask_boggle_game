from flask import Flask, render_template, session, request, jsonify
from boggle import Boggle

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret'

boggle_game = Boggle()

@app.route('/')
def homepage():
    '''show game'''
    board = boggle_game.make_board()
    session['board'] = board
    
    highscore = session.get('highscore', 0)
    nplays = session.get('nplay', 0)

    return render_template('app.html', board = board, 
                           highscore = highscore, nplays=nplays)


@app.route('/check-word')
def check_word():
    '''check if the word is in dictionary'''

    word = request.args['add-word']
    board = session['board']
    response = boggle_game.check_valid_word(board, word)

    return jsonify({'result': response})


@app.route('/post-score', methods = ['POST'])
def post_score():
    score = request.json["score"]
    highscore = session.get("highscore", 0)
    nplays = session.get("nplays", 0)

    session['nplays'] = nplays + 1
    session['highscore'] = max(score, highscore)

    return jsonify(brokeRecord=score > highscore)