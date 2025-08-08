from datetime import datetime
from . import db

class Produit(db.Model):
    __tablename__ = 'produits'
    
    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    prix_unitaire = db.Column(db.Float, nullable=False)  # Prix en ariary
    stock_actuel = db.Column(db.Integer, default=0)
    stock_minimum = db.Column(db.Integer, default=5)
    categorie = db.Column(db.String(50))
    code_produit = db.Column(db.String(50), unique=True)
    date_creation = db.Column(db.DateTime, default=datetime.utcnow)
    actif = db.Column(db.Boolean, default=True)
    
    # Relations
    lignes_vente = db.relationship('LigneVente', backref='produit', lazy=True)
    
    @property
    def stock_faible(self):
        return self.stock_actuel <= self.stock_minimum
    
    def __repr__(self):
        return f'<Produit {self.nom}>'

class Client(db.Model):
    __tablename__ = 'clients'
    
    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120))
    telephone = db.Column(db.String(20))
    adresse = db.Column(db.Text)
    ville = db.Column(db.String(50))
    code_postal = db.Column(db.String(10))
    date_creation = db.Column(db.DateTime, default=datetime.utcnow)
    actif = db.Column(db.Boolean, default=True)
    
    # Relations
    ventes = db.relationship('Vente', backref='client', lazy=True)
    
    def __repr__(self):
        return f'<Client {self.nom}>'

class Vente(db.Model):
    __tablename__ = 'ventes'
    
    id = db.Column(db.Integer, primary_key=True)
    numero_vente = db.Column(db.String(50), unique=True, nullable=False)
    client_id = db.Column(db.Integer, db.ForeignKey('clients.id'), nullable=False)
    date_vente = db.Column(db.DateTime, default=datetime.utcnow)
    total_ht = db.Column(db.Float, default=0.0)  # Montant hors taxe en ariary
    taux_tva = db.Column(db.Float, default=20.0)  # Taux de TVA en pourcentage
    total_ttc = db.Column(db.Float, default=0.0)  # Montant TTC en ariary
    statut = db.Column(db.String(20), default='confirmée')  # confirmée, annulée
    notes = db.Column(db.Text)
    
    # Relations
    lignes = db.relationship('LigneVente', backref='vente', lazy=True, cascade='all, delete-orphan')
    facture = db.relationship('Facture', backref='vente', uselist=False, lazy=True)
    
    def calculer_totaux(self):
        """Calcule les totaux HT et TTC basés sur les lignes de vente"""
        self.total_ht = sum(ligne.sous_total for ligne in self.lignes)
        self.total_ttc = self.total_ht * (1 + self.taux_tva / 100)
    
    def __repr__(self):
        return f'<Vente {self.numero_vente}>'

class LigneVente(db.Model):
    __tablename__ = 'lignes_vente'
    
    id = db.Column(db.Integer, primary_key=True)
    vente_id = db.Column(db.Integer, db.ForeignKey('ventes.id'), nullable=False)
    produit_id = db.Column(db.Integer, db.ForeignKey('produits.id'), nullable=False)
    quantite = db.Column(db.Integer, nullable=False)
    prix_unitaire = db.Column(db.Float, nullable=False)  # Prix au moment de la vente
    sous_total = db.Column(db.Float, nullable=False)
    
    def __init__(self, **kwargs):
        super(LigneVente, self).__init__(**kwargs)
        if self.prix_unitaire and self.quantite:
            self.sous_total = self.prix_unitaire * self.quantite
    
    def __repr__(self):
        return f'<LigneVente {self.quantite} x {self.produit.nom if self.produit else "Produit"}>'

class Facture(db.Model):
    __tablename__ = 'factures'
    
    id = db.Column(db.Integer, primary_key=True)
    numero_facture = db.Column(db.String(50), unique=True, nullable=False)
    vente_id = db.Column(db.Integer, db.ForeignKey('ventes.id'), nullable=False)
    date_facture = db.Column(db.DateTime, default=datetime.utcnow)
    date_echeance = db.Column(db.DateTime)
    statut = db.Column(db.String(20), default='impayée')  # impayée, payée, en_retard
    notes = db.Column(db.Text)
    
    def __repr__(self):
        return f'<Facture {self.numero_facture}>'