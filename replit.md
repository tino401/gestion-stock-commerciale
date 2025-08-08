# Overview

This is a commercial management system (Gestion Commerciale) built with Flask that helps businesses manage products, clients, sales, and invoicing. The application provides a comprehensive dashboard with sales statistics, inventory management with low stock alerts, client management, and automated invoice generation with PDF export capabilities. It's designed for small to medium businesses needing to track their commercial operations efficiently.

# User Preferences

Preferred communication style: Simple, everyday language.

# System Architecture

## Backend Architecture
- **Flask Web Framework**: Core web application using Flask with SQLAlchemy ORM for database operations
- **Database Layer**: SQLAlchemy with declarative base model, configured to support both SQLite (development) and PostgreSQL (production) via DATABASE_URL environment variable
- **Model Structure**: Four main entities - Produit (Product), Client, Vente (Sale), LigneVente (Sale Line), and Facture (Invoice) with proper relationships
- **Connection Pooling**: Configured with pool recycling and pre-ping for database reliability

## Frontend Architecture
- **Template Engine**: Jinja2 templates with a base template system for consistent UI
- **CSS Framework**: Bootstrap dark theme optimized for Replit with custom CSS overrides
- **JavaScript Enhancement**: Custom JavaScript for improved interactivity, form validation, and user experience
- **Responsive Design**: Mobile-first approach using Bootstrap grid system

## Data Management
- **Inventory Tracking**: Real-time stock levels with automatic low stock alerts and minimum stock thresholds
- **Sales Processing**: Multi-line sales with automatic total calculations including TVA (VAT) support
- **Client Management**: Complete customer database with contact information and sales history

## PDF Generation
- **ReportLab Integration**: Professional invoice PDF generation with company branding and structured layout
- **Document Management**: Automatic invoice numbering system with date-based formatting

## Business Logic
- **Stock Management**: Automatic stock level updates on sales with low stock warnings
- **Pricing System**: Ariary (MGA) currency formatting with proper number formatting utilities
- **Sales Workflow**: Complete sales cycle from quotation to invoice with status tracking

# External Dependencies

## Python Libraries
- **Flask**: Web framework with SQLAlchemy extension for ORM
- **ReportLab**: PDF generation for invoices and reports
- **Werkzeug**: WSGI utilities including ProxyFix for deployment

## Frontend Libraries
- **Bootstrap**: UI framework with dark theme from Replit CDN
- **Font Awesome**: Icon library for consistent iconography throughout the application
- **JavaScript**: Vanilla JavaScript for client-side functionality

## Database
- **SQLite**: Default development database (fallback)
- **PostgreSQL**: Production database support via DATABASE_URL environment variable

## Development Environment
- **Replit**: Configured for Replit hosting with appropriate proxy fixes and environment variable support
- **Environment Configuration**: Flexible configuration supporting both development and production environments