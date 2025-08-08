from datetime import datetime
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.pdfgen import canvas
from io import BytesIO
import uuid

def generer_numero_vente():
    """Génère un numéro de vente unique basé sur la date et un UUID court"""
    today = datetime.now()
    date_str = today.strftime('%Y%m%d')
    uuid_court = str(uuid.uuid4())[:8].upper()
    return f"VTE-{date_str}-{uuid_court}"

def generer_numero_facture():
    """Génère un numéro de facture unique basé sur la date et un UUID court"""
    today = datetime.now()
    date_str = today.strftime('%Y%m%d')
    uuid_court = str(uuid.uuid4())[:8].upper()
    return f"FACT-{date_str}-{uuid_court}"

def formater_ariary(montant):
    """Formate un montant en ariary avec séparateurs de milliers"""
    return f"{montant:,.0f} MGA".replace(',', ' ')

def generer_facture_pdf(facture):
    """Génère le PDF d'une facture"""
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4)
    styles = getSampleStyleSheet()
    story = []
    
    # Style personnalisé pour le titre
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=20,
        textColor=colors.blue,
        spaceAfter=30,
        alignment=1  # Centré
    )
    
    # En-tête de la facture
    story.append(Paragraph("FACTURE", title_style))
    story.append(Spacer(1, 20))
    
    # Informations de la facture
    facture_info = [
        ["Numéro de facture:", facture.numero_facture],
        ["Date de facture:", facture.date_facture.strftime('%d/%m/%Y')],
        ["Date d'échéance:", facture.date_echeance.strftime('%d/%m/%Y') if facture.date_echeance else "N/A"],
        ["Statut:", facture.statut.upper()]
    ]
    
    table_info = Table(facture_info, colWidths=[2*inch, 3*inch])
    table_info.setStyle(TableStyle([
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 12),
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
    ]))
    
    story.append(table_info)
    story.append(Spacer(1, 30))
    
    # Informations du client
    client = facture.vente.client
    story.append(Paragraph("Informations Client", styles['Heading2']))
    
    client_info = [
        ["Nom:", client.nom],
        ["Email:", client.email or "N/A"],
        ["Téléphone:", client.telephone or "N/A"],
        ["Adresse:", client.adresse or "N/A"]
    ]
    
    table_client = Table(client_info, colWidths=[1.5*inch, 3.5*inch])
    table_client.setStyle(TableStyle([
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
    ]))
    
    story.append(table_client)
    story.append(Spacer(1, 30))
    
    # Détails des produits
    story.append(Paragraph("Détails de la commande", styles['Heading2']))
    
    # En-tête du tableau des produits
    data = [['Produit', 'Quantité', 'Prix unitaire', 'Sous-total']]
    
    for ligne in facture.vente.lignes:
        data.append([
            ligne.produit.nom,
            str(ligne.quantite),
            formater_ariary(ligne.prix_unitaire),
            formater_ariary(ligne.sous_total)
        ])
    
    # Ligne des totaux
    data.append(['', '', 'Total HT:', formater_ariary(facture.vente.total_ht)])
    data.append(['', '', f'TVA ({facture.vente.taux_tva}%):', formater_ariary(facture.vente.total_ttc - facture.vente.total_ht)])
    data.append(['', '', 'Total TTC:', formater_ariary(facture.vente.total_ttc)])
    
    table_produits = Table(data, colWidths=[3*inch, 1*inch, 1.5*inch, 1.5*inch])
    table_produits.setStyle(TableStyle([
        # En-tête
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 12),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        
        # Corps du tableau
        ('FONTNAME', (0, 1), (-1, -4), 'Helvetica'),
        ('FONTSIZE', (0, 1), (-1, -4), 10),
        ('ALIGN', (0, 1), (0, -4), 'LEFT'),  # Nom du produit aligné à gauche
        
        # Lignes de totaux
        ('FONTNAME', (0, -3), (-1, -1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, -3), (-1, -1), 11),
        ('ALIGN', (2, -3), (-1, -1), 'RIGHT'),
        
        # Bordures
        ('GRID', (0, 0), (-1, -4), 1, colors.black),
        ('LINEBELOW', (0, -3), (-1, -1), 2, colors.black),
    ]))
    
    story.append(table_produits)
    story.append(Spacer(1, 30))
    
    # Notes si présentes
    if facture.notes:
        story.append(Paragraph("Notes", styles['Heading2']))
        story.append(Paragraph(facture.notes, styles['Normal']))
    
    # Générer le PDF
    doc.build(story)
    buffer.seek(0)
    return buffer.getvalue()
