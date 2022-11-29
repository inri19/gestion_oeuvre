from flask import Blueprint, render_template, request, flash, redirect, url_for
from pymongo import MongoClient
from datetime import datetime

connection_string = "mongodb+srv://<cluster_name>:<password>@cluster0.zjpto59.mongodb.net/?retryWrites=true&w=majority"
client = MongoClient(connection_string)
date_str = str(datetime.now()).split(" ")[0]

musee = client.musee

manage = Blueprint('manage', __name__)

@manage.route('/manage')
def admin():

    return render_template('gestion/gestion.html')

# NEW
@manage.route('/manage/new')
def new():

    nb_piece = musee.piece.count_documents({})
    nb_artiste = musee.piece.count_documents({})
    bolo = False

    # Display the last element
    # print(f"Display : {musee.oeuvre.find()[musee.oeuvre.count_documents({})-1]}")

    if nb_artiste > 0 and nb_piece > 0 :

        bolo = True

    return render_template('gestion/nouveau.html', bolo = bolo)

@manage.route('/manage/new/room', methods=['GET', 'POST'])
def new_room():

    piece = musee.piece

    if request.method == "POST" :

        nom = request.form.get('nom_piece')
        description = request.form.get('description')
        image = request.form.get('img')

        if len(nom) == 0 or len(image) == 0 :

            flash('Les champs nom et image sont obligatoire', category='error')
        
        else :

            if len(description) == 0 :

                piece_doc = { "nom" : nom, "description" : "aucune" , "img_lien" : image, "date_creation" : date_str }
            
            else :

                piece_doc = { "nom" : nom, "description" : description, "img_lien" : image, "date_creation" : date_str }

            
            if musee.piece.count_documents({}) == 0 :

                piece.insert_one({ "_id" : 0, "nom" : "Entrepot", "description" : "Toutes oeuvres sans piece sont envoyé ici", "date_creation" : date_str })
                piece_doc['_id'] = 1
            
            else :

                piece_doc['_id'] = musee.piece.find()[musee.piece.count_documents({})-1]['_id'] + 1 
                
            piece.insert_one(piece_doc)


            flash('Piece Enregistrer', category='success')    


    return render_template('gestion/nouvelle_piece.html')

@manage.route('/manage/new/artist', methods=['POST', 'GET'])
def new_artist():

    author = musee.author

    if request.method == "POST" :

        nom = request.form.get('nom')
        prenom = request.form.get('prenom')
        pays = request.form.get('pays_nat')
        periode = request.form.get('periode_art')
        image = request.form.get('img')
        desciption = request.form.get('description')
        deces = request.form.get('annee_mort')

        if len(nom) == 0 or len(prenom) == 0 or len(pays) == 0 or len(periode) == 0 or len(image) == 0 or len(desciption) == 0 or len(deces) == 0 :

            flash('Tous les champs sont obligatoires', category='error')

        else :

            if musee.author.count_documents({}) == 0 :

                artist_doc = { "_id" : 0, "nom" : nom, "prenom" : prenom, "pays" : pays, "periode" : periode, "img_lien" : image, "description" : desciption, "deces" : int(deces) }
            
            else :

                last_id = musee.author.find()[musee.author.count_documents({})-1]['_id']
                artist_doc = { "_id" : last_id+1, "nom" : nom, "prenom" : prenom, "pays" : pays, "periode" : periode, "img_lien" : image, "description" : desciption, "deces" : int(deces) }

            author.insert_one(artist_doc)

            flash('Artiste Enregistrer', category='success')


    return render_template('gestion/nouveau_artiste.html')

@manage.route('/manage/new/oeuvre', methods=['POST', 'GET'])
def new_oeuvre():

    columns = {"_id" : 1, "nom" : 1}
    auteurs = musee.author.find({}, columns)
    pieces = musee.piece.find({}, columns)

    oeuvre = musee.oeuvre

    if request.method == "POST" :

        nom = request.form.get('nom')
        type = request.form.get('type')
        image = request.form.get('img')
        description = request.form.get('description')
        annee = request.form.get('annee')
        auteur = request.form.get('auteur')
        piece = request.form.get('piece')


        if len(nom) == 0 or len(type) == 0 or len(image) == 0 or len(description) == 0 or len(annee) == 0 :

            flash('Tous les champs sont obligatoires', category='error')
        
        else :

            if musee.oeuvre.count_documents({}) == 0 :

                oeuvre_doc = {"_id" : 0, "nom" : nom, "type" : type, "img_lien" : image, "description" : description, "annee" : int(annee), "auteur" : int(auteur), "piece" : int(piece) , "date_creation" : date_str}
            
            else :

                last_id = musee.oeuvre.find()[musee.oeuvre.count_documents({})-1]['_id']
                oeuvre_doc = { "_id" : last_id+1, "nom" : nom, "type" : type, "img_lien" : image, "description" : description, "annee" : int(annee), "auteur" : int(auteur), "piece" : int(piece) , "date_creation" : date_str}

            oeuvre.insert_one(oeuvre_doc)

            flash('Oeuvre Enregistrer !', category='success')



    return render_template('gestion/nouvelle_oeuvre.html', auteurs=auteurs, pieces=pieces)

# UPDATE

@manage.route('/manage/update')
def update():

    return render_template('gestion/modifier.html')

@manage.route('/manage/update/room')
def update_room():

    pieces = musee.piece.find()

    return render_template('gestion/modifier_piece.html', pieces=pieces)

@manage.route('/manage/update/oeuvre')
def update_oeuvre():

    dict_oeuvres = {}
    oeuvres = musee.oeuvre.find()

    
    for i in range(musee.oeuvre.count_documents(filter={})) :

        _id_auteur = int(oeuvres[i]['auteur'])
        _id_piece = int(oeuvres[i]['piece'])
        auteur = musee.author.find_one({ "_id" : _id_auteur })
        piece = musee.piece.find_one({ "_id" : _id_piece })

        dict_oeuvres[i] = { "id" : oeuvres[i]['_id'], "nom" : oeuvres[i]['nom'], "type" : oeuvres[i]['type'], "description" : oeuvres[i]['description'], "annee" : oeuvres[i]['annee'], "auteur" : f"{auteur['nom']} {auteur['prenom']}", "piece" : piece['nom'] }
    

    return render_template('gestion/modifier_oeuvre.html', oeuvres = dict_oeuvres)

@manage.route('/manage/update/artist')
def update_artist():

    flash('Attention lorsque vous supprimer un artiste toutes ses oeuvres seront egalement supprimer !!', category='error')

    artists = musee.author.find()

    return render_template('gestion/modifier_artiste.html', artists=artists)

@manage.route('/manage/update/room/<_id>', methods=['POST', 'GET'])
def update_room_details(_id):

    _id = int(_id)

    piece = musee.piece.find_one({ "_id" : _id })

    if request.method == 'POST' :

        nom = request.form.get('nom_piece')
        description = request.form.get('description')
        image = request.form.get('img')

        
        if len(nom) == 0 or len(image) == 0 :

            flash('Les champs nom et image sont obligatoire', category='error')
        
        else :

            if len(description) == 0 :

                piece_update = { "$set" : {"nom" : nom, "description" : "aucune" , "img_lien" : image} }
            
            else :

                piece_update = { "$set" : {"nom" : nom, "description" : description, "img_lien" : image} }
            
            musee.piece.update_one({ "_id" : _id }, piece_update)
            # piece.update_one({ "_id" : _id }, piece_update)

            flash('Piece Modifier', category='success')
        

    return render_template('gestion/form_modifier_piece.html', piece=piece)

@manage.route('/manage/update/oeuvre/<_id>', methods=['POST', 'GET'])
def update_oeuvre_details(_id):

    _id = int(_id)
    oeuvre = musee.oeuvre.find_one({ "_id" : _id })
    auteurs = musee.author.find()
    pieces = musee.piece.find()

    if request.method == 'POST':

        nom = request.form.get('nom')
        type = request.form.get('type')
        image = request.form.get('img')
        description = request.form.get('description')
        annee = request.form.get('annee')
        auteur = request.form.get('auteur')
        piece = request.form.get('piece')

        if len(nom) == 0 or len(type) == 0 or len(image) == 0 or len(description) == 0 or len(annee) == 0 :

            flash('Tous les champs sont obligatoires', category='error')
        
        else :

            oeuvre_update = { "$set" : { "nom" : nom, "type" : type, "img_lien" : image, "description" : description, "annee" : int(annee), "auteur" : int(auteur), "piece" : int(piece) } }
            musee.oeuvre.update_one({ "_id" : _id }, oeuvre_update)

            flash('Oeuvre Modifier !', category='success')

    return render_template('gestion/form_modifier_oeuvre.html', oeuvre=oeuvre, auteurs=auteurs, pieces=pieces)

@manage.route('/manage/update/artist/<_id>', methods=['POST', 'GET'])
def update_artist_details(_id):

    _id = int(_id)

    artist = musee.author.find_one({ "_id" : _id })

    if request.method == 'POST':

        nom = request.form.get('nom')
        prenom = request.form.get('prenom')
        pays = request.form.get('pays_nat')
        periode = request.form.get('periode_art')
        image = request.form.get('img')
        desciption = request.form.get('description')
        deces = request.form.get('annee_mort')

        if len(nom) == 0 or len(prenom) == 0 or len(pays) == 0 or len(periode) == 0 or len(image) == 0 or len(desciption) == 0 or len(deces) == 0 :

            flash('Tous les champs sont obligatoires', category='error')

        else :

            artist_update = { "$set" : { "nom" : nom, "prenom" : prenom, "pays" : pays, "periode" : periode, "img_lien" : image, "description" : desciption, "deces" : int(deces) } }
            musee.author.update_one({ "_id" : _id }, artist_update)

            flash('Artiste Modifier', category='success')
        

    return render_template('gestion/form_modifier_artiste.html', artist=artist)

# DELETE

@manage.route('/manage/delete/room/<_id>', methods=['POST', 'GET'])
def delete_room(_id):

    _id = int(_id)

    if musee.oeuvre.find({ "piece" : _id }) :

        oeuvre_update = { "$set" : { "piece" : 0 } }
        musee.oeuvre.update_many({ "piece" : _id }, oeuvre_update)

    musee.piece.delete_one({ "_id" : _id })

    flash('Piece Supprimer', category='success')

    return redirect(url_for('manage.update_room'))

@manage.route('/manage/delete/oeuvre/<_id>', methods=['POST', 'GET'])
def delete_oeuvre(_id):

    _id = int(_id)

    musee.oeuvre.delete_one({ "_id" : _id })

    flash('Oeuvre supprimer', category='success')

    return redirect(url_for('manage.update_oeuvre'))

@manage.route('/manage/delete/artist/<_id>', methods=['POST', 'GET'])
def delete_artist(_id):

    _id = int(_id)
    query = { 'auteur' : _id }

    musee.author.delete_one({ "_id" : _id })
    musee.oeuvre.delete_many(query)

    flash('Artiste Supprimer', category='success')

    return redirect(url_for('manage.update_artist'))