from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from sqlalchemy import and_
from .. import db
from ..models import Produit

produits_bp = Blueprint('produits', __name__, url_prefix='/produits')

@produits_bp.route('/')
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

@produits_bp.route('/ajouter', methods=['GET', 'POST'])
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
            return redirect(url_for('produits.produits'))
            
        except Exception as e:
            db.session.rollback()
            flash(f'Erreur lors de l\'ajout du produit: {str(e)}', 'error')
    
    return render_template('ajouter_produit.html')

@produits_bp.route('/modifier/<int:id>', methods=['GET', 'POST'])
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
            return redirect(url_for('produits.produits'))
            
        except Exception as e:
            db.session.rollback()
            flash(f'Erreur lors de la modification du produit: {str(e)}', 'error')
    
    return render_template('modifier_produit.html', produit=produit)

@produits_bp.route('/supprimer/<int:id>', methods=['POST'])
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
    
    return redirect(url_for('produits.produits'))

# API endpoints pour AJAX
@produits_bp.route('/api/<int:id>')
def api_produit_detail(id):
    """API pour obtenir les détails d'un produit"""
    produit = Produit.query.get_or_404(id)
    return jsonify({
        'id': produit.id,
        'nom': produit.nom,
        'prix_unitaire': produit.prix_unitaire,
        'stock_actuel': produit.stock_actuel
    })