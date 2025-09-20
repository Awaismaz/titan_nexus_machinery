# Titan Nexus Industrial Supply Platform
 
Titan Nexus Industrial Supply is a Django-powered operations console and marketing site for a heavy machinery general order supplier. It blends a conversion-focused landing page with a maintainable backend for catalogue management, industrial content, and custom procurement requests.
 
## Highlights
- Story-driven landing page with hero metrics, industry showcases, value propositions, testimonials, partner carousel, and FAQ knowledge base.
- Dynamic catalogue featuring advanced filters (category, industry, availability, financing, power range), detail views, related assets, and collateral downloads.
- Custom request workflow capturing budgets, timelines, capacity needs, attachments, and auto-logging status history ready for follow-up from the Django admin.
- Admin experience optimised with inlines for hero content, machine galleries, lifecycle services, and partner logos. Site settings are singleton-backed for easy edits.
- Seeded showcase content including AI-authored About narrative, differentiators, testimonials, industries, and flagship machines so the UI renders fully populated out of the box.
 
## Tech Stack
- Python 3.10 / Django 4.2
- Bootstrap 5, Font Awesome, custom CSS for a dark, marketing-friendly aesthetic
- Crispy Forms (Bootstrap 5), django-widget-tweaks, Pillow
 
## Local Setup
1. Activate the provided Conda environment (named machine) with Python 3.10.
2. Install dependencies:
    pip install -r requirements.txt
3. Run migrations:
    python manage.py migrate
4. Populate showcase content:
    python manage.py seed_data
5. Optional – create an admin user to manage content:
    python manage.py createsuperuser
6. Launch the development server:
    python manage.py runserver
 
Access the site at http://127.0.0.1:8000/ and the admin at http://127.0.0.1:8000/admin/.
 
## Content Management
- Update branding, hero copy, stats, contact details, and About narrative via Site Settings (singleton model) in the admin.
- Hero metrics, value propositions, service offerings, industries, partners, and FAQs are all editable collections.
- Machines support multi-industry tags, gallery images, downloadable documents, featured badges, financing flags, and highlight ribbons.
- Custom requests are tracked with status pipelines and automated log creation for each state change.
 
## Utilities
- python manage.py seed_data – idempotent command to (re)apply rich sample data for demos or fresh databases.
- CSS assets live in static/css/main.css; hero imagery can be uploaded through admin and is served via /media/ in development.
 
## Next Ideas
- Vendor and client authentication portals with dashboards.
- Automated proposal PDF generation from custom requests.
- Integration hooks for ERP, CRM, or marketing automation platforms.
- Multilingual landing experiences aligned with target regions.
