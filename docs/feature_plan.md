# Feature & Experience Blueprint

## Brand Identity
- **Suggested Name:** Titan Nexus Industrial Supply
- **Tagline:** "Powering Production with Precision Partnerships"
- **Visual Direction:** Bold slate and electric orange palette, geometric machinery accents, modern sans-serif typography (e.g., Poppins / Montserrat), Font Awesome iconography.

## Core Platform Goals
1. Present compelling marketing landing page tailored for industrial procurement stakeholders.
2. Centralize machinery catalogue with rich media and taxonomy for multi-industry vendors.
3. Enable inbound custom-machine requests with backend workflow support.
4. Provide maintainable CMS-like controls via Django Admin for all dynamic content.

## User Personas
- **Industrial Buyer / Vendor:** Needs to browse catalogue, evaluate credibility, request custom machines.
- **Sales & Procurement Team:** Manages listings, responds to requests, updates testimonials, hero content.
- **Operations Manager:** Tracks request pipeline, updates fulfilment status.

## Feature Breakdown

### 1. Landing Page Experience
- Hero section with animated background overlay, key metrics, CTA buttons ('View Catalogue', 'Request Custom Build').
- Featured categories using iconography (Font Awesome) and count of available machines per category.
- "Why Titan Nexus" value propositions with quick stats (years in service, orders fulfilled, partner OEMs).
- Dynamic carousel of hero product highlights (admin-configurable highlight flag).
- AI-generated testimonials with client industry tags and rating badges.
- "Industries We Serve" grid with icons and blurbs (editable via admin).
- Partner logos strip (image uploads managed in admin).
- Call-to-action footer with contact email, WhatsApp/phone, enquiry CTA.

### 2. Product Catalogue
- Machine model listing with thumbnail, short specs, availability tag, and quick action links.
- Detail page containing gallery carousel, specifications table, downloadable brochure (file upload).
- Filtering by category, industry compatibility, power rating range, and availability.
- Search (full-text across name, manufacturer, model number, keywords).
- Featured/highlighted badges & financing badge flag.

### 3. Custom Request Workflow
- Frontend form capturing industry, required machine type, budget range, production capacity, timeline, file attachments.
- Automatic email notification placeholder (config-ready) + admin list view for tracking.
- Status pipeline (New, Under Review, Quoted, Fulfilled) editable in admin.
- Request detail admin page with internal notes.

### 4. Content Management via Admin
- Manage hero banner copy, metrics, contact info (SiteSettings singleton model).
- Manage testimonials, industry focus areas, partner logos.
- Manage FAQ entries (for landing page accordion).
- Manage highlight machines and categories.
- Rich-text support for About Us/Experience sections (Markdown/TextField with sanitized output).

### 5. Supporting Features
- Global navigation with logo (SVG) + sticky behavior.
- Responsive layout (Bootstrap 5 + custom SCSS compiled to CSS).
- Lazy-loaded images, consistent card components.
- SEO meta tags, OpenGraph data from settings.
- Footer with quick links, contact, newsletter CTA.
- 404/500 branded error pages.

## Data Model Overview
- SiteSettings: hero_title, hero_subtitle, hero_cta_primary, contact_email, contact_phone, whatsapp_link, stats (JSON).
- Industry: name, description, icon (Font Awesome class), order.
- Category: name, slug, description, icon, display_order.
- Machine: name, slug, category FK, industries M2M, short_description, description, specifications (JSON/structured), price_from, availability_status, is_featured, highlight_text, hero_image, gallery (through MachineImage).
- MachineDocument: machine FK, file, label.
- MachineImage: machine FK, image, caption, display_order.
- Testimonial: client_name, client_role, company, industry FK, rating, quote, avatar.
- Partner: name, website, logo.
- FAQ: question, answer, display_order.
- CustomRequest: created_at, name, company, email, phone, industry FK, machine_type, capacity_requirement, budget_range, timeline, description, attachment, status, internal_notes.
- RequestStatusLog: request FK, status, comment, timestamp.

## Content Strategy
- Seed admin fixtures for testimonials, industries, FAQs, hero metrics, dummy machines.
- AI-crafted About Us, Experience narrative placed in SiteSettings fields.
- Unique testimonial blurbs per sector (e.g., Automotive, Food Processing, Renewable Energy).

## Technical Stack Decisions
- Django 4.2 LTS for stability with Python 3.10.
- PostgreSQL-ready configuration but default to SQLite for local.
- Django Crispy Forms + Bootstrap 5 for polished form UI.
- Pillow for image handling; django-widget-tweaks for template form control.
- Use django-storages friendly abstractions (placeholder for future cloud adoption).

## Roadmap Enhancements (Post-MVP)
- Quote PDF generation for custom requests.
- Inventory integration via ERP API.
- Auth portal for returning vendors.
- Integration with marketing automation (HubSpot/Zapier).
- Multilingual support and geo-targeted case studies.