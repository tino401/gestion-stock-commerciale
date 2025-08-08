from flask import render_template, request, redirect, url_for, flash, jsonify, make_response
from datetime import datetime, timedelta
from sqlalchemy import func, and_, extract
from app import app, db
from models import Produit, Client, Vente, LigneVente, Facture
import utils

@app.route('/')
def index():
    """Page d'accueil avec statistiques générales"""
    # Statistiques générales
    total_produits = Produit.query.filter_by(actif=True).count()
    total_clients = Client.query.filter_by(actif=True).count()
    
    # Produits en stock faible
    produits_stock_faible = Produit.query.filter(
        and_(Produit.stock_actuel <= Produit.stock_minimum, Produit.actif == True)
    ).all()
    
    # Ventes du mois en cours
    debut_mois = datetime.now().replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    ventes_mois = db.session.query(func.sum(Vente.total_ttc)).filter(
        and_(Vente.date_vente >= debut_mois, Vente.statut == 'confirmée')
    ).scalar() or 0
    
    # Ventes du jour
    debut_jour = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
    ventes_jour = db.session.query(func.sum(Vente.total_ttc)).filter(
        and_(Vente.date_vente >= debut_jour, Vente.statut == 'confirmée')
    ).scalar() or 0
    
    return render_template('index.html',
                         total_produits=total_produits,
                         total_clients=total_clients,
                         produits_stock_faible=produits_stock_faible,
                         ventes_mois=ventes_mois,
                         ventes_jour=ventes_jour)

@app.route('/produits')
def produits():
    """Liste des produits"""
    search = request.args.get('search', '')
    categorie = request.args.get('categorie', '')
    
    query = Produit.query.filter_by(actif=True)
    
    if search:
        query = query.filter(Produit.nom.contains(search))
    
    if categorie:
        query = query.filter_by(categorie=categorie)
    
    produits = query.order_by(Produit.nom).all()
    categories = db.session.query(Produit.categorie).distinct().filter(Produit.categorie.isnot(None)).all()
    categories = [cat[0] for cat in categories]
    
    return render_template('produits.html', produits=produits, categories=categories)

@app.route('/produits/ajouter', methods=['GET', 'POST'])
def ajouter_produit():
    """Ajouter un nouveau produit"""
    if request.method == 'POST':
        try:
            produit = Produit(
                nom=request.form['nom'],
                description=request.form.get('description', ''),
                prix_unitaire=float(request.form['prix_unitaire']),
                stock_actuel=int(request.form.get('stock_actuel', 0)),
                stock_minimum=int(request.form.get('stock_minimum', 5)),
                categorie=request.form.get('categorie', ''),
                code_produit=request.form.get('code_produit', '')
            )
            
            db.session.add(produit)
            db.session.commit()
            flash('Produit ajouté avec succès!', 'success')
            return redirect(url_for('produits'))
            
        except Exception as e:
            db.session.rollback()
            flash(f'Erreur lors de l\'ajout du produit: {str(e)}', 'error')
    
    return render_template('ajouter_produit.html')

@app.route('/produits/modifier/<int:id>', methods=['GET', 'POST'])
def modifier_produit(id):
    """Modifier un produit existant"""
    produit = Produit.query.get_or_404(id)
    
    if request.method == 'POST':
        try:
            produit.nom = request.form['nom']
            produit.description = request.form.get('description', '')
            produit.prix_unitaire = float(request.form['prix_unitaire'])
            produit.stock_actuel = int(request.form.get('stock_actuel', 0))
            produit.stock_minimum = int(request.form.get('stock_minimum', 5))
            produit.categorie = request.form.get('categorie', '')
            produit.code_produit = request.form.get('code_produit', '')
            
            db.session.commit()
            flash('Produit modifié avec succès!', 'success')
            return redirect(url_for('produits'))
            
        except Exception as e:
            db.session.rollback()
            flash(f'Erreur lors de la modification du produit: {str(e)}', 'error')
    
    return render_template('modifier_produit.html', produit=produit)

@app.route('/produits/supprimer/<int:id>', methods=['POST'])
def supprimer_produit(id):
    """Supprimer (désactiver) un produit"""
    try:
        produit = Produit.query.get_or_404(id)
        produit.actif = False
        db.session.commit()
        flash('Produit supprimé avec succès!', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Erreur lors de la suppression du produit: {str(e)}', 'error')
    
    return redirect(url_for('produits'))

@app.route('/clients')
def clients():
    """Liste des clients"""
    search = request.args.get('search', '')
    
    query = Client.query.filter_by(actif=True)
    
    if search:
        query = query.filter(Client.nom.contains(search))
    
    clients = query.order_by(Client.nom).all()
    
    return render_template('clients.html', clients=clients)

@app.route('/clients/ajouter', methods=['GET', 'POST'])
def ajouter_client():
    """Ajouter un nouveau client"""
    if request.method == 'POST':
        try:
            client = Client(
                nom=request.form['nom'],
                email=request.form.get('email', ''),
                telephone=request.form.get('telephone', ''),
                adresse=request.form.get('adresse', ''),
                ville=request.form.get('ville', ''),
                code_postal=request.form.get('code_postal', '')
            )
            
            db.session.add(client)
            db.session.commit()
            flash('Client ajouté avec succès!', 'success')
            return redirect(url_for('clients'))
            
        except Exception as e:
            db.session.rollback()
            flash(f'Erreur lors de l\'ajout du client: {str(e)}', 'error')
    
    return render_template('ajouter_client.html')

@app.route('/clients/supprimer/<int:id>', methods=['POST'])
def supprimer_client(id):
    """Supprimer (désactiver) un client"""
    try:
        client = Client.query.get_or_404(id)
        client.actif = False
        db.session.commit()
        flash('Client supprimé avec succès!', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Erreur lors de la suppression du client: {str(e)}', 'error')
    
    return redirect(url_for('clients'))

@app.route('/ventes')
def ventes():
    """Liste des ventes"""
    date_debut = request.args.get('date_debut')
    date_fin = request.args.get('date_fin')
    client_id = request.args.get('client_id')
    
    query = Vente.query
    
    if date_debut:
        query = query.filter(Vente.date_vente >= datetime.strptime(date_debut, '%Y-%m-%d'))
    
    if date_fin:
        fin = datetime.strptime(date_fin, '%Y-%m-%d') + timedelta(days=1)
        query = query.filter(Vente.date_vente < fin)
    
    if client_id:
        query = query.filter_by(client_id=int(client_id))
    
    ventes = query.order_by(Vente.date_vente.desc()).all()
    clients = Client.query.filter_by(actif=True).order_by(Client.nom).all()
    
    return render_template('ventes.html', ventes=ventes, clients=clients)

@app.route('/ventes/nouvelle', methods=['GET', 'POST'])
def nouvelle_vente():
    """Créer une nouvelle vente"""
    if request.method == 'POST':
        try:
            # Générer un numéro de vente unique
            numero_vente = utils.generer_numero_vente()
            
            vente = Vente(
                numero_vente=numero_vente,
                client_id=int(request.form['client_id']),
                taux_tva=float(request.form.get('taux_tva', 20.0)),
                notes=request.form.get('notes', '')
            )
            
            db.session.add(vente)
            db.session.flush()  # Pour obtenir l'ID de la vente
            
            # Ajouter les lignes de vente
            produits_ids = request.form.getlist('produit_id')
            quantites = request.form.getlist('quantite')
            
            for i, produit_id in enumerate(produits_ids):
                if produit_id and quantites[i]:
                    produit = Produit.query.get(int(produit_id))
                    quantite = int(quantites[i])
                    
                    # Vérifier le stock
                    if produit.stock_actuel < quantite:
                        flash(f'Stock insuffisant pour {produit.nom}. Stock disponible: {produit.stock_actuel}', 'error')
                        db.session.rollback()
                        return redirect(url_for('nouvelle_vente'))
                    
                    ligne = LigneVente(
                        vente_id=vente.id,
                        produit_id=int(produit_id),
                        quantite=quantite,
                        prix_unitaire=produit.prix_unitaire
                    )
                    ligne.sous_total = ligne.prix_unitaire * ligne.quantite
                    
                    # Mettre à jour le stock
                    produit.stock_actuel -= quantite
                    
                    db.session.add(ligne)
            
            # Calculer les totaux
            vente.calculer_totaux()
            
            # Créer la facture automatiquement
            facture = Facture(
                numero_facture=utils.generer_numero_facture(),
                vente_id=vente.id,
                date_echeance=datetime.utcnow() + timedelta(days=30)
            )
            
            db.session.add(facture)
            db.session.commit()
            
            flash('Vente créée avec succès!', 'success')
            return redirect(url_for('facture_detail', id=facture.id))
            
        except Exception as e:
            db.session.rollback()
            flash(f'Erreur lors de la création de la vente: {str(e)}', 'error')
    
    clients = Client.query.filter_by(actif=True).order_by(Client.nom).all()
    produits = Produit.query.filter_by(actif=True).order_by(Produit.nom).all()
    
    return render_template('nouvelle_vente.html', clients=clients, produits=produits)

@app.route('/factures')
def factures():
    """Liste des factures"""
    statut = request.args.get('statut')
    
    query = Facture.query
    
    if statut:
        query = query.filter_by(statut=statut)
    
    factures = query.order_by(Facture.date_facture.desc()).all()
    
    return render_template('factures.html', factures=factures)

@app.route('/factures/<int:id>')
def facture_detail(id):
    """Détail d'une facture"""
    facture = Facture.query.get_or_404(id)
    return render_template('facture_detail.html', facture=facture)

@app.route('/factures/<int:id>/pdf')
def facture_pdf(id):
    """Générer le PDF d'une facture"""
    facture = Facture.query.get_or_404(id)
    
    try:
        pdf_content = utils.generer_facture_pdf(facture)
        
        response = make_response(pdf_content)
        response.headers['Content-Type'] = 'application/pdf'
        response.headers['Content-Disposition'] = f'inline; filename="facture_{facture.numero_facture}.pdf"'
        
        return response
        
    except Exception as e:
        flash(f'Erreur lors de la génération du PDF: {str(e)}', 'error')
        return redirect(url_for('facture_detail', id=id))

@app.route('/factures/<int:id>/statut', methods=['POST'])
def modifier_statut_facture(id):
    """Modifier le statut d'une facture"""
    try:
        facture = Facture.query.get_or_404(id)
        nouveau_statut = request.form['statut']
        
        if nouveau_statut in ['impayée', 'payée', 'en_retard']:
            facture.statut = nouveau_statut
            db.session.commit()
            flash('Statut de la facture modifié avec succès!', 'success')
        else:
            flash('Statut invalide!', 'error')
            
    except Exception as e:
        db.session.rollback()
        flash(f'Erreur lors de la modification du statut: {str(e)}', 'error')
    
    return redirect(url_for('facture_detail', id=id))

@app.route('/rapports')
def rapports():
    """Page des rapports et statistiques"""
    # Rapport mensuel
    mois_actuel = datetime.now().month
    annee_actuelle = datetime.now().year
    
    # Ventes par mois (12 derniers mois)
    ventes_mensuelles = []
    for i in range(12):
        mois = mois_actuel - i
        annee = annee_actuelle
        
        if mois <= 0:
            mois += 12
            annee -= 1
        
        total = db.session.query(func.sum(Vente.total_ttc)).filter(
            and_(
                extract('month', Vente.date_vente) == mois,
                extract('year', Vente.date_vente) == annee,
                Vente.statut == 'confirmée'
            )
        ).scalar() or 0
        
        ventes_mensuelles.insert(0, {
            'mois': f"{annee}-{mois:02d}",
            'total': total
        })
    
    # Produits les plus vendus
    produits_vendus = db.session.query(
        Produit.nom,
        func.sum(LigneVente.quantite).label('total_vendu')
    ).join(LigneVente).join(Vente).filter(
        Vente.statut == 'confirmée'
    ).group_by(Produit.id, Produit.nom).order_by(
        func.sum(LigneVente.quantite).desc()
    ).limit(10).all()
    
    # Clients les plus actifs
    clients_actifs = db.session.query(
        Client.nom,
        func.count(Vente.id).label('nb_ventes'),
        func.sum(Vente.total_ttc).label('total_achats')
    ).join(Vente).filter(
        Vente.statut == 'confirmée'
    ).group_by(Client.id, Client.nom).order_by(
        func.sum(Vente.total_ttc).desc()
    ).limit(10).all()
    
    return render_template('rapports.html',
                         ventes_mensuelles=ventes_mensuelles,
                         produits_vendus=produits_vendus,
                         clients_actifs=clients_actifs)

# API endpoints pour AJAX
@app.route('/api/produit/<int:id>')
def api_produit_detail(id):
    """API pour obtenir les détails d'un produit"""
    produit = Produit.query.get_or_404(id)
    return jsonify({
        'id': produit.id,
        'nom': produit.nom,
        'prix_unitaire': produit.prix_unitaire,
        'stock_actuel': produit.stock_actuel
    })
