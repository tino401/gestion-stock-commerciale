from flask import Blueprint, render_template, request, redirect, url_for, flash
from .. import db
from ..models import Client

clients_bp = Blueprint('clients', __name__, url_prefix='/clients')

@clients_bp.route('/')
def clients():
    """Liste des clients"""
    search = request.args.get('search', '')
    
    query = Client.query.filter_by(actif=True)
    
    if search:
        query = query.filter(Client.nom.contains(search))
    
    clients = query.order_by(Client.nom).all()
    
    return render_template('clients.html', clients=clients)

@clients_bp.route('/ajouter', methods=['GET', 'POST'])
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
            return redirect(url_for('clients.clients'))
            
        except Exception as e:
            db.session.rollback()
            flash(f'Erreur lors de l\'ajout du client: {str(e)}', 'error')
    
    return render_template('ajouter_client.html')

@clients_bp.route('/supprimer/<int:id>', methods=['POST'])
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
    
    return redirect(url_for('clients.clients'))