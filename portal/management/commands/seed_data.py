from decimal import Decimal

from django.core.management.base import BaseCommand

from portal.models import (
    Category,
    HeroMetric,
    Industry,
    Machine,
    Partner,
    FAQ,
    ServiceOffering,
    SiteSettings,
    Testimonial,
    ValueProposition,
)


class Command(BaseCommand):
    help = 'Seed the database with showcase content for Titan Nexus Industrial Supply.'

    def handle(self, *args, **options):
        settings = SiteSettings.load()
        settings.tagline = 'Powering production with precision partnerships'
        settings.hero_title = 'Heavy machinery, delivered with intelligence'
        settings.hero_subtitle = (
            'We orchestrate sourcing, inspection, and commissioning for capital equipment across automotive, food, energy, and process industries.'
        )
        settings.primary_cta_label = 'Explore Catalogue'
        settings.primary_cta_link = '/catalogue/'
        settings.secondary_cta_label = 'Request Custom Build'
        settings.secondary_cta_link = '/custom-request/'
        settings.about_title = 'AI-accelerated general order suppliers'
        settings.about_body = (
            'Titan Nexus Industrial Supply unites procurement strategists, automation engineers, and logistics specialists to shorten the path between requirement and production impact. '
            'Our AI-driven vendor intelligence graph evaluates cost, compliance, and uptime history across 420+ OEM relationships, enabling clients to deploy machinery that performs at scale.'
        )
        settings.experience_highlight = (
            'Dedicated launch pods in Karachi, Dubai, and Rotterdam manage factory acceptance testing, duty drawback, and last-mile commissioning.'
        )
        settings.experience_years = 18
        settings.machines_deployed = 486
        settings.uptime_commitment = '99.2% fleet uptime guarantee'
        settings.response_time = 'Quote turnaround in under 24 hours'
        settings.contact_email = 'engage@titannexus.co'
        settings.contact_phone = '+92 300 1234567'
        settings.whatsapp_link = 'https://wa.me/971501234567'
        settings.operation_regions = 'Pakistan, GCC, Europe, North America'
        settings.support_hours = 'Global support 24/7'
        settings.newsletter_blurb = 'Insights on capital projects, predictive maintenance, and financing strategies delivered monthly.'
        settings.footer_statement = 'Certified general order supplier for critical industries with dual-shore execution teams.'
        settings.save()

        metrics = [
            ('Global deployments delivered', '480+', 'fa-solid fa-earth-americas'),
            ('Average commissioning lead time', '11.4 weeks', 'fa-solid fa-stopwatch'),
            ('OEM alliances under SLA', '126', 'fa-solid fa-handshake-angle'),
        ]
        HeroMetric.objects.filter(settings=settings).exclude(label__in=[m[0] for m in metrics]).delete()
        for order, (label, value, icon) in enumerate(metrics, start=1):
            HeroMetric.objects.update_or_create(
                settings=settings,
                label=label,
                defaults={'value': value, 'icon': icon, 'display_order': order},
            )

        value_props = [
            ('Predictive procurement intelligence', 'Every RFQ flows through our machine-learning engine that benchmarks technical fit, landed cost, and uptime probabilities before you ever speak to suppliers.', 'fa-solid fa-brain'),
            ('Inspection-first assurance', 'Resident QA teams oversee FAT, NDT, and regulatory documentation so your assets clear compliance and start-up faster.', 'fa-solid fa-shield-check'),
            ('Lifecycle performance control', 'Commissioning engineers, spare-parts buffers, and condition monitoring dashboards keep the fleet running with 99% availability.', 'fa-solid fa-arrows-rotate'),
            ('Flexible commercial pathways', 'Own, lease, or outcome-based contracting—financing desks tailor capital strategy to your balance sheet.', 'fa-solid fa-scale-balanced'),
        ]
        ValueProposition.objects.filter(settings=settings).exclude(title__in=[vp[0] for vp in value_props]).delete()
        for order, (title, description, icon) in enumerate(value_props, start=1):
            ValueProposition.objects.update_or_create(
                settings=settings,
                title=title,
                defaults={'description': description, 'icon': icon, 'display_order': order},
            )

        services = [
            ('Specification engineering', 'Translate production goals into technical specs, power loads, and compliance matrices.', 'fa-solid fa-compass-drafting'),
            ('Supplier vetting & audits', 'AI-ranked shortlist plus boots-on-ground audits to de-risk supplier selection.', 'fa-solid fa-microscope'),
            ('Project logistics & commissioning', 'Door-to-line execution with erection crews, training, and performance ramp plans.', 'fa-solid fa-truck-ramp-box'),
            ('Lifecycle analytics', 'IoT retrofits and CMMS tie-ins ensure uptime, energy, and OEE dashboards stay visible.', 'fa-solid fa-chart-line'),
        ]
        ServiceOffering.objects.exclude(title__in=[s[0] for s in services]).delete()
        for order, (title, description, icon) in enumerate(services, start=1):
            ServiceOffering.objects.update_or_create(
                title=title,
                defaults={'description': description, 'icon': icon, 'display_order': order},
            )

        industries = [
            ('Automotive & EV', 'High-throughput assembly, lightweighting, and battery module integration lines ready for ramp.', 'fa-solid fa-car-on', 'Launched 5 giga-scale welding programs in 18 months.'),
            ('Food & Beverage', 'CIP-ready processing, aseptic filling, and cold-chain automation tailored to HACCP standards.', 'fa-solid fa-bottle-water', 'Zero-recall track record across three continents.'),
            ('Renewable Energy', 'Solar glass laminators, blade fabrication, and grid-scale battery pack assembly cells.', 'fa-solid fa-solar-panel', 'Supplying the top five utility-scale EPCs.'),
            ('Pharmaceutical', 'GMP-compliant reactors, blister lines, and clean-room handling with global validation.', 'fa-solid fa-pills', 'Validated by WHO prequalification auditors.'),
            ('Construction Materials', 'Bulk powder plants, precast automation, and mobile batching units with rapid deployment.', 'fa-solid fa-city', 'Delivered 2.4M tons annual capacity in 2023.'),
            ('Logistics & Warehousing', 'Automated storage, AMR fleets, and vision-enabled sortation for omni-channel retailers.', 'fa-solid fa-boxes-stacked', 'Boosted fulfillment efficiency by 33% avg.'),
        ]
        for order, (name, description, icon, feature) in enumerate(industries, start=1):
            Industry.objects.update_or_create(
                name=name,
                defaults={'description': description, 'icon': icon, 'feature_statement': feature, 'display_order': order},
            )

        categories = [
            ('Automation Lines', 'Robotic and vision-enabled production lines ready for turnkey deployment.', 'fa-solid fa-robot'),
            ('Processing Systems', 'Thermal, mixing, and chemical processing skid systems with full validation.', 'fa-solid fa-industry'),
            ('Material Handling', 'Smart conveyors, ASRS, and palletization systems for discrete and process industries.', 'fa-solid fa-dolly'),
            ('Energy & Utilities', 'Power conditioning, compressed air, and waste-to-energy systems for plant resilience.', 'fa-solid fa-bolt'),
        ]
        category_lookup = {}
        for order, (name, description, icon) in enumerate(categories, start=1):
            category, _ = Category.objects.update_or_create(
                name=name,
                defaults={'description': description, 'icon': icon, 'display_order': order},
            )
            category_lookup[name] = category

        industry_lookup = {industry.name: industry for industry in Industry.objects.all()}

        machine_payloads = [
            {
                'name': 'HyperForge Robotic Welding Cell',
                'category': category_lookup['Automation Lines'],
                'industries': ['Automotive & EV', 'Construction Materials'],
                'short_description': 'Modular MIG/TIG welding cell with adaptive vision for high-mix chassis fabrication.',
                'description': 'Deliver flawless weld integrity with AI-guided torch paths, dual-station fixtures, and integrated fume extraction designed for 24/7 operations.',
                'features': [
                    'Adaptive torch compensation using thermal camera feedback',
                    'Cycle analytics via integrated MES connector',
                    'Tool-less fixture swaps under 3 minutes',
                ],
                'model_number': 'HF-4200X',
                'manufacturer': 'Titan Nexus Robotics Consortium',
                'power_rating_kw': Decimal('65'),
                'capacity_output': '28 chassis/hour',
                'price_from': Decimal('320000'),
                'lead_time_weeks': 10,
                'warranty_months': 24,
                'availability_status': 'in_stock',
                'highlight_text': 'EV-ready welding intelligence',
                'is_featured': True,
                'financing_available': True,
            },
            {
                'name': 'AquaPure CIP Skid 4.0',
                'category': category_lookup['Processing Systems'],
                'industries': ['Food & Beverage', 'Pharmaceutical'],
                'short_description': 'Smart clean-in-place skid with recipe automation and sustainability analytics.',
                'description': 'Reduce changeover time with auto-validated CIP cycles, remote diagnostics, and water reclamation technology tuned for regulated environments.',
                'features': [
                    'PID control with digital twin simulations',
                    'Validated reporting aligned with FDA 21 CFR Part 11',
                    '30% water reclamation via closed-loop filtration',
                ],
                'model_number': 'CIP-4K',
                'manufacturer': 'Nexus Fluid Systems',
                'power_rating_kw': Decimal('32'),
                'capacity_output': 'Up to 4 concurrent circuits',
                'price_from': Decimal('185000'),
                'lead_time_weeks': 12,
                'warranty_months': 18,
                'availability_status': 'back_order',
                'highlight_text': 'Sustainability optimized',
                'is_featured': True,
                'financing_available': False,
            },
            {
                'name': 'HeliosSmart Solar Glass Laminator',
                'category': category_lookup['Energy & Utilities'],
                'industries': ['Renewable Energy'],
                'short_description': 'High-throughput laminator delivering premium solar glass modules with inline QC.',
                'description': 'Designed for utility-scale players seeking precision lamination with minimal scrap and automated defect rejection using spectral cameras.',
                'features': [
                    '4-lane lamination with automatic EVA alignment',
                    'Spectral inspection rejecting defects under 0.2mm',
                    'Edge sealing robot with adaptive thermal profile',
                ],
                'model_number': 'HX-GL720',
                'manufacturer': 'Helios Manufacturing Alliance',
                'power_rating_kw': Decimal('120'),
                'capacity_output': '720 modules/shift',
                'price_from': Decimal('540000'),
                'lead_time_weeks': 16,
                'warranty_months': 36,
                'availability_status': 'custom_build',
                'highlight_text': 'Utility-scale throughput',
                'is_featured': True,
                'financing_available': True,
            },
        ]
        newline = chr(10)
        for payload in machine_payloads:
            industries = payload.pop('industries', [])
            features = payload.pop('features', [])
            payload['key_features'] = newline.join(features)
            machine, _ = Machine.objects.update_or_create(
                name=payload['name'],
                defaults=payload,
            )
            machine.industries.set([industry_lookup[name] for name in industries if name in industry_lookup])
        testimonials = [
            {
                'client_name': 'Amelia Hart',
                'client_role': 'VP Operations',
                'company': 'NovaVolt Mobility',
                'industry': 'Automotive & EV',
                'quote': 'Titan Nexus compressed our welding line deployment from 22 to 12 weeks and handed over with OEE north of 92% on day one.',
                'rating': 5,
                'highlight': True,
            },
            {
                'client_name': 'Dr. Rizwan Malik',
                'client_role': 'Head of Manufacturing Science',
                'company': 'PureLife Nutraceuticals',
                'industry': 'Food & Beverage',
                'quote': 'Their CIP skid arrived audit-ready with digital validation packs. We cleared EU inspections without a single deviation.',
                'rating': 5,
                'highlight': True,
            },
            {
                'client_name': 'Sofia El-Amin',
                'client_role': 'Chief Projects Officer',
                'company': 'Aurora Renewables',
                'industry': 'Renewable Energy',
                'quote': 'HeliosSmart laminators from Titan Nexus pushed our module output up 38% while cutting scrap in half.',
                'rating': 4,
                'highlight': False,
            },
        ]
        for testimonial in testimonials:
            industry = industry_lookup.get(testimonial.pop('industry'))
            Testimonial.objects.update_or_create(
                client_name=testimonial['client_name'],
                company=testimonial['company'],
                defaults={**testimonial, 'industry': industry},
            )

        partners = [
            ('Siemens Motion Alliance', 'https://siemens.com'),
            ('Atlas Robotics Consortium', 'https://atlas-robotics.example'),
            ('Helios Manufacturing Alliance', 'https://helios-industries.example'),
            ('PureFlow Process Equipment', 'https://pureflow.example'),
        ]
        for order, (name, website) in enumerate(partners, start=1):
            Partner.objects.update_or_create(
                name=name,
                defaults={'website': website, 'display_order': order, 'caption': ''},
            )

        faqs = [
            ('How fast can you mobilise a sourcing project?', 'Our launch desk produces a comparative sourcing dossier within 5 working days, including technical evaluation, landed cost, and risk scoring.'),
            ('Do you support factory acceptance tests and audits?', 'Yes, QA engineers run FAT protocols, third-party inspections, and virtual factory walk-throughs so stakeholders can sign-off with confidence.'),
            ('Can Titan Nexus arrange financing or leasing?', 'We partner with regional lenders and export credit agencies to structure capex-light options including operating leases and performance-based contracts.'),
            ('What after-sales support is included?', 'Each deployment includes spare strategy, remote monitoring enablement, and optional resident engineers for the first 90 days of production.'),
        ]
        for order, (question, answer) in enumerate(faqs, start=1):
            FAQ.objects.update_or_create(
                question=question,
                defaults={'answer': answer, 'display_order': order},
            )

        self.stdout.write(self.style.SUCCESS('Seed data successfully applied.'))
