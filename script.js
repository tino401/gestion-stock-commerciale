/* JavaScript personnalisé pour Gestion Commerciale */
/* Améliore l'interactivité et l'expérience utilisateur */

// ===== INITIALISATION GLOBALE =====
document.addEventListener('DOMContentLoaded', function() {
    initializeApp();
});

function initializeApp() {
    // Initialiser les tooltips Bootstrap
    initializeTooltips();
    
    // Initialiser les popovers
    initializePopovers();
    
    // Auto-masquage des alertes
    autoHideAlerts();
    
    // Formatage des nombres
    formatNumbers();
    
    // Amélioration des formulaires
    enhanceForms();
    
    // Animations d'entrée
    animateElements();
}

// ===== TOOLTIPS ET POPOVERS =====
function initializeTooltips() {
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
}

function initializePopovers() {
    const popoverTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="popover"]'));
    popoverTriggerList.map(function (popoverTriggerEl) {
        return new bootstrap.Popover(popoverTriggerEl);
    });
}

// ===== GESTION DES ALERTES =====
function autoHideAlerts() {
    const alerts = document.querySelectorAll('.alert:not(.alert-permanent)');
    alerts.forEach(function(alert) {
        // Auto-masquage après 5 secondes pour les alertes de succès
        if (alert.classList.contains('alert-success')) {
            setTimeout(function() {
                const bsAlert = new bootstrap.Alert(alert);
                bsAlert.close();
            }, 5000);
        }
        
        // Auto-masquage après 8 secondes pour les autres alertes
        else if (!alert.classList.contains('alert-danger')) {
            setTimeout(function() {
                const bsAlert = new bootstrap.Alert(alert);
                bsAlert.close();
            }, 8000);
        }
    });
}

// Fonction pour afficher une alerte personnalisée
function showAlert(message, type = 'info', permanent = false) {
    const alertContainer = document.querySelector('.container.mt-4');
    if (!alertContainer) return;
    
    const alertId = 'alert-' + Date.now();
    const alertHtml = `
        <div id="${alertId}" class="alert alert-${type} alert-dismissible fade show ${permanent ? 'alert-permanent' : ''}" role="alert">
            ${message}
            <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
        </div>
    `;
    
    alertContainer.insertAdjacentHTML('afterbegin', alertHtml);
    
    if (!permanent) {
        setTimeout(function() {
            const alert = document.getElementById(alertId);
            if (alert) {
                const bsAlert = new bootstrap.Alert(alert);
                bsAlert.close();
            }
        }, type === 'success' ? 5000 : 8000);
    }
}

// ===== FORMATAGE DES NOMBRES =====
function formatNumbers() {
    // Formater tous les montants en ariary
    const montants = document.querySelectorAll('[data-currency="MGA"]');
    montants.forEach(function(element) {
        const value = parseFloat(element.textContent.replace(/[^\d.-]/g, ''));
        if (!isNaN(value)) {
            element.textContent = formatMGA(value);
        }
    });
}

function formatMGA(amount) {
    return new Intl.NumberFormat('fr-FR').format(amount) + ' MGA';
}

function parseMGA(text) {
    return parseFloat(text.replace(/[^\d.-]/g, '')) || 0;
}

// ===== AMÉLIORATION DES FORMULAIRES =====
function enhanceForms() {
    // Validation en temps réel
    const forms = document.querySelectorAll('form');
    forms.forEach(function(form) {
        form.addEventListener('submit', function(e) {
            if (!form.checkValidity()) {
                e.preventDefault();
                e.stopPropagation();
                showAlert('Veuillez corriger les erreurs dans le formulaire.', 'warning');
            }
            form.classList.add('was-validated');
        });
    });
    
    // Formatage automatique des prix
    const prixInputs = document.querySelectorAll('input[name*="prix"], input[id*="prix"]');
    prixInputs.forEach(function(input) {
        input.addEventListener('blur', function() {
            const value = parseFloat(this.value);
            if (!isNaN(value) && value >= 0) {
                // Afficher une info-bulle avec le montant formaté
                this.setAttribute('title', formatMGA(value));
                this.setAttribute('data-bs-toggle', 'tooltip');
                new bootstrap.Tooltip(this);
            }
        });
    });
    
    // Auto-complétion intelligente pour les codes produits
    const codeInputs = document.querySelectorAll('input[name="code_produit"]');
    codeInputs.forEach(function(input) {
        input.addEventListener('blur', function() {
            if (!this.value) {
                // Générer un code automatique basé sur le nom
                const nomInput = this.form.querySelector('input[name="nom"]');
                if (nomInput && nomInput.value) {
                    const code = generateProductCode(nomInput.value);
                    this.value = code;
                }
            }
        });
    });
}

function generateProductCode(nom) {
    // Générer un code produit basé sur le nom
    const words = nom.trim().toUpperCase().split(/\s+/);
    let code = '';
    
    if (words.length === 1) {
        code = words[0].substring(0, 6);
    } else if (words.length === 2) {
        code = words[0].substring(0, 3) + words[1].substring(0, 3);
    } else {
        code = words.slice(0, 3).map(w => w.charAt(0)).join('') + 
               words[0].substring(1, 4);
    }
    
    // Ajouter un suffixe numérique
    const timestamp = Date.now().toString().slice(-3);
    return code + timestamp;
}

// ===== ANIMATIONS =====
function animateElements() {
    // Animer les cartes au chargement
    const cards = document.querySelectorAll('.card');
    cards.forEach(function(card, index) {
        card.style.animationDelay = (index * 0.1) + 's';
        card.classList.add('slide-in');
    });
    
    // Observer pour animer les éléments au scroll
    if ('IntersectionObserver' in window) {
        const observer = new IntersectionObserver(function(entries) {
            entries.forEach(function(entry) {
                if (entry.isIntersecting) {
                    entry.target.classList.add('fade-in');
                    observer.unobserve(entry.target);
                }
            });
        }, {
            threshold: 0.1
        });
        
        const elementsToAnimate = document.querySelectorAll('.table, .alert, .btn-group');
        elementsToAnimate.forEach(function(el) {
            observer.observe(el);
        });
    }
}

// ===== GESTION DES TABLEAUX =====
function initializeTableFeatures() {
    // Tri des colonnes (version simple)
    const sortableHeaders = document.querySelectorAll('th[data-sort]');
    sortableHeaders.forEach(function(header) {
        header.style.cursor = 'pointer';
        header.addEventListener('click', function() {
            sortTable(this);
        });
        
        // Ajouter un indicateur visuel
        header.innerHTML += ' <i class="fas fa-sort text-muted"></i>';
    });
}

function sortTable(header) {
    // Implémentation simple du tri
    const table = header.closest('table');
    const tbody = table.querySelector('tbody');
    const rows = Array.from(tbody.querySelectorAll('tr'));
    const columnIndex = Array.from(header.parentNode.children).indexOf(header);
    const sortType = header.dataset.sort;
    
    const sortedRows = rows.sort(function(a, b) {
        const aVal = a.children[columnIndex].textContent.trim();
        const bVal = b.children[columnIndex].textContent.trim();
        
        if (sortType === 'number') {
            return parseFloat(aVal.replace(/[^\d.-]/g, '')) - parseFloat(bVal.replace(/[^\d.-]/g, ''));
        } else {
            return aVal.localeCompare(bVal, 'fr');
        }
    });
    
    // Alterner l'ordre
    if (header.dataset.sortDirection === 'desc') {
        sortedRows.reverse();
        header.dataset.sortDirection = 'asc';
        header.querySelector('i').className = 'fas fa-sort-up';
    } else {
        header.dataset.sortDirection = 'desc';
        header.querySelector('i').className = 'fas fa-sort-down';
    }
    
    // Réorganiser les lignes
    sortedRows.forEach(function(row) {
        tbody.appendChild(row);
    });
}

// ===== RECHERCHE EN TEMPS RÉEL =====
function initializeLiveSearch() {
    const searchInputs = document.querySelectorAll('input[type="search"], input[name="search"]');
    searchInputs.forEach(function(input) {
        let searchTimeout;
        input.addEventListener('input', function() {
            clearTimeout(searchTimeout);
            searchTimeout = setTimeout(function() {
                performLiveSearch(input);
            }, 300);
        });
    });
}

function performLiveSearch(input) {
    const searchTerm = input.value.toLowerCase();
    const targetTable = document.querySelector('table tbody');
    
    if (targetTable) {
        const rows = targetTable.querySelectorAll('tr');
        let visibleCount = 0;
        
        rows.forEach(function(row) {
            const text = row.textContent.toLowerCase();
            if (text.includes(searchTerm)) {
                row.style.display = '';
                visibleCount++;
            } else {
                row.style.display = 'none';
            }
        });
        
        // Afficher un message si aucun résultat
        const existingNoResult = targetTable.querySelector('.no-results');
        if (existingNoResult) {
            existingNoResult.remove();
        }
        
        if (visibleCount === 0 && searchTerm !== '') {
            const noResultRow = document.createElement('tr');
            noResultRow.className = 'no-results';
            noResultRow.innerHTML = `
                <td colspan="100%" class="text-center text-muted py-4">
                    <i class="fas fa-search fa-2x mb-2"></i><br>
                    Aucun résultat trouvé pour "${input.value}"
                </td>
            `;
            targetTable.appendChild(noResultRow);
        }
    }
}

// ===== UTILITAIRES DE CONFIRMATION =====
function confirmerAction(message, callback) {
    if (confirm(message)) {
        callback();
    }
}

function confirmerSuppressionAvecModal(id, nom, type = 'élément') {
    const modal = new bootstrap.Modal(document.createElement('div'));
    const modalHtml = `
        <div class="modal fade" tabindex="-1">
            <div class="modal-dialog">
                <div class="modal-content">
                    <div class="modal-header bg-danger text-white">
                        <h5 class="modal-title">
                            <i class="fas fa-exclamation-triangle me-2"></i>
                            Confirmer la suppression
                        </h5>
                        <button type="button" class="btn-close btn-close-white" data-bs-dismiss="modal"></button>
                    </div>
                    <div class="modal-body">
                        <p>Êtes-vous sûr de vouloir supprimer ${type} "<strong>${nom}</strong>" ?</p>
                        <div class="alert alert-warning">
                            <i class="fas fa-info-circle me-2"></i>
                            Cette action ne peut pas être annulée.
                        </div>
                    </div>
                    <div class="modal-footer">
                        <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">
                            <i class="fas fa-times me-1"></i>Annuler
                        </button>
                        <button type="button" class="btn btn-danger" onclick="executerSuppression(${id})">
                            <i class="fas fa-trash me-1"></i>Supprimer définitivement
                        </button>
                    </div>
                </div>
            </div>
        </div>
    `;
    
    document.body.insertAdjacentHTML('beforeend', modalHtml);
    const modalElement = document.body.lastElementChild;
    const modalInstance = new bootstrap.Modal(modalElement);
    modalInstance.show();
    
    // Nettoyer après fermeture
    modalElement.addEventListener('hidden.bs.modal', function() {
        modalElement.remove();
    });
}

// ===== COPIER DANS LE PRESSE-PAPIER =====
function copierTexte(text) {
    if (navigator.clipboard) {
        navigator.clipboard.writeText(text).then(function() {
            showAlert('Texte copié dans le presse-papier !', 'success');
        });
    } else {
        // Fallback pour les navigateurs plus anciens
        const textArea = document.createElement('textarea');
        textArea.value = text;
        document.body.appendChild(textArea);
        textArea.select();
        document.execCommand('copy');
        document.body.removeChild(textArea);
        showAlert('Texte copié dans le presse-papier !', 'success');
    }
}

// ===== EXPORT DE DONNÉES =====
function exporterTableauCSV(tableId, fileName = 'export') {
    const table = document.getElementById(tableId) || document.querySelector('table');
    if (!table) return;
    
    let csv = [];
    const rows = table.querySelectorAll('tr');
    
    rows.forEach(function(row) {
        const cols = row.querySelectorAll('th, td');
        const rowData = [];
        cols.forEach(function(col) {
            // Nettoyer le texte (supprimer les balises HTML)
            let text = col.textContent.trim();
            // Échapper les guillemets
            text = text.replace(/"/g, '""');
            rowData.push('"' + text + '"');
        });
        csv.push(rowData.join(','));
    });
    
    const csvContent = csv.join('\n');
    const blob = new Blob([csvContent], { type: 'text/csv;charset=utf-8;' });
    const link = document.createElement('a');
    
    if (link.download !== undefined) {
        const url = URL.createObjectURL(blob);
        link.setAttribute('href', url);
        link.setAttribute('download', fileName + '.csv');
        link.style.visibility = 'hidden';
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
        
        showAlert('Tableau exporté avec succès !', 'success');
    }
}

// ===== RACCOURCIS CLAVIER =====
document.addEventListener('keydown', function(e) {
    // Ctrl+S pour sauvegarder les formulaires
    if (e.ctrlKey && e.key === 's') {
        e.preventDefault();
        const submitBtn = document.querySelector('button[type="submit"]');
        if (submitBtn) {
            submitBtn.click();
        }
    }
    
    // Échap pour fermer les modales
    if (e.key === 'Escape') {
        const openModals = document.querySelectorAll('.modal.show');
        openModals.forEach(function(modal) {
            const modalInstance = bootstrap.Modal.getInstance(modal);
            if (modalInstance) {
                modalInstance.hide();
            }
        });
    }
    
    // Ctrl+F pour focus sur la recherche
    if (e.ctrlKey && e.key === 'f') {
        const searchInput = document.querySelector('input[type="search"], input[name="search"]');
        if (searchInput) {
            e.preventDefault();
            searchInput.focus();
            searchInput.select();
        }
    }
});

// ===== IMPRESSION AMÉLIORÉE =====
function imprimerFacture() {
    // Masquer les éléments non nécessaires avant impression
    const elementsToHide = document.querySelectorAll('.btn, .alert, .navbar, .dropdown');
    elementsToHide.forEach(el => el.style.display = 'none');
    
    window.print();
    
    // Remettre les éléments après impression
    setTimeout(function() {
        elementsToHide.forEach(el => el.style.display = '');
    }, 1000);
}

// ===== STATISTIQUES EN TEMPS RÉEL =====
function mettreAJourStatistiques() {
    // Cette fonction peut être appelée périodiquement pour mettre à jour
    // les statistiques sans recharger la page
    fetch('/api/stats')
        .then(response => response.json())
        .then(data => {
            // Mettre à jour les cartes de statistiques
            const elements = {
                'total_produits': data.total_produits,
                'total_clients': data.total_clients,
                'ventes_jour': formatMGA(data.ventes_jour),
                'ventes_mois': formatMGA(data.ventes_mois)
            };
            
            Object.keys(elements).forEach(key => {
                const element = document.getElementById(key);
                if (element) {
                    element.textContent = elements[key];
                }
            });
        })
        .catch(error => {
            console.log('Erreur lors de la mise à jour des statistiques:', error);
        });
}

// ===== GESTION DU CACHE =====
function viderCacheLocal() {
    if (localStorage) {
        localStorage.clear();
        showAlert('Cache local vidé avec succès !', 'info');
    }
}

// ===== DÉTECTION DE CONNEXION =====
window.addEventListener('online', function() {
    showAlert('Connexion rétablie !', 'success');
});

window.addEventListener('offline', function() {
    showAlert('Connexion perdue. Certaines fonctionnalités peuvent être limitées.', 'warning', true);
});

// ===== FONCTIONS GLOBALES EXPOSÉES =====
window.GestionCommerciale = {
    showAlert: showAlert,
    formatMGA: formatMGA,
    parseMGA: parseMGA,
    copierTexte: copierTexte,
    exporterTableauCSV: exporterTableauCSV,
    imprimerFacture: imprimerFacture,
    confirmerAction: confirmerAction,
    viderCacheLocal: viderCacheLocal
};

// ===== INITIALISATION FINALE =====
// Auto-initialiser certaines fonctionnalités quand le DOM est prêt
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', function() {
        initializeLiveSearch();
        initializeTableFeatures();
    });
} else {
    initializeLiveSearch();
    initializeTableFeatures();
}

console.log('🏪 Gestion Commerciale - JavaScript chargé avec succès !');
