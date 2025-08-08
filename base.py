from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify, make_response
from datetime import datetime, timedelta
from sqlalchemy import func, and_, extract
from .. import db
from ..models import Produit, Client, Vente, LigneVente, Facture
from .. import utils

base_bp = Blueprint('base', __name__)

@base_bp.route('/')
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

@base_bp.route('/factures')
def factures():
    """Liste des factures"""
    statut = request.args.get('statut')
    
    query = Facture.query
    
    if statut:
        query = query.filter_by(statut=statut)
    
    factures = query.order_by(Facture.date_facture.desc()).all()
    
    return render_template('factures.html', factures=factures)

@base_bp.route('/factures/<int:id>')
def facture_detail(id):
    """Détail d'une facture"""
    facture = Facture.query.get_or_404(id)
    return render_template('facture_detail.html', facture=facture)

@base_bp.route('/factures/<int:id>/pdf')
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
        return redirect(url_for('base.facture_detail', id=id))

@base_bp.route('/factures/<int:id>/statut', methods=['POST'])
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
    
    return redirect(url_for('base.facture_detail', id=id))

@base_bp.route('/rapports')
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