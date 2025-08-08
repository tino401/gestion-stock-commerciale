from flask import Blueprint, render_template, request, redirect, url_for, flash
from datetime import datetime, timedelta
from .. import db
from ..models import Produit, Client, Vente, LigneVente, Facture
from .. import utils

ventes_bp = Blueprint('ventes', __name__, url_prefix='/ventes')

@ventes_bp.route('/')
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

@ventes_bp.route('/nouvelle', methods=['GET', 'POST'])
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
                        return redirect(url_for('ventes.nouvelle_vente'))
                    
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
            return redirect(url_for('base.facture_detail', id=facture.id))
            
        except Exception as e:
            db.session.rollback()
            flash(f'Erreur lors de la création de la vente: {str(e)}', 'error')
    
    clients = Client.query.filter_by(actif=True).order_by(Client.nom).all()
    produits = Produit.query.filter_by(actif=True).order_by(Produit.nom).all()
    
    return render_template('nouvelle_vente.html', clients=clients, produits=produits)