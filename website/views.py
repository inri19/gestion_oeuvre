from flask import Blueprint, render_template
from pymongo import MongoClient
from random import randint

connection_string = "mongodb+srv://<cluster_name>:<password>@cluster0.zjpto59.mongodb.net/?retryWrites=true&w=majority"
client = MongoClient(connection_string)
musee = client.musee

views = Blueprint('views', __name__)

@views.route('/')
def home():

    return render_template('accueil.html')

@views.route('/piece')
def piece():

    pieces = []

    for item in musee.piece.find().sort('_id', -1) :

        if item['_id'] == 0 :

            pass

        else : 

            pieces.append(item)

    return render_template('vue/piece.html', tab_pieces=pieces)

@views.route('/piece/<_id>')
def piece_details(_id):

    piece = musee.piece.find_one({ "_id" : int(_id) })
    oeuvres = musee.oeuvre.find({ "piece" : int(_id) }).sort('_id', -1)

    print(piece)
    print(oeuvres)

    return render_template('vue/piece_details.html', piece=piece, oeuvres=oeuvres)

@views.route('/oeuvre')
def oeuvre():

    return render_template('vue/oeuvre.html', tab_oeuvres=musee.oeuvre.find().sort('_id', -1))

@views.route('/oeuvre/<_id>')
def oeuvre_details(_id):

    _id = int(_id)

    oeuvre = musee.oeuvre.find_one({ "_id" : _id })

    id_auteur = oeuvre['auteur']
    artiste = musee.author.find_one({ "_id" : int(id_auteur)})

    id_piece = oeuvre['piece']
    piece = musee.piece.find_one({ "_id" : int(id_piece) })

    return render_template('vue/oeuvre_details.html', oeuvre=oeuvre, artiste=artiste, piece=piece)

@views.route('/decouverte')
def decouverte():

    auteurs = musee.author.find()
    nb_auteurs = musee.author.count_documents(filter={})
    auteur = auteurs[randint(0,nb_auteurs)]

    return render_template('vue/decouverte.html', auteur=auteur)