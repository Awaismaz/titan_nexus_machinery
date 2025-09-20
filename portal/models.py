from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.utils.crypto import get_random_string
from django.utils.text import slugify


class SingletonModel(models.Model):
    """Abstract base to enforce a single row that can be updated via admin."""

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        self.pk = 1
        super().save(*args, **kwargs)

    @classmethod
    def load(cls):
        obj, _ = cls.objects.get_or_create(pk=1)
        return obj


class SiteSettings(SingletonModel):
    business_name = models.CharField(max_length=120, default='Titan Nexus Industrial Supply')
    tagline = models.CharField(max_length=160, blank=True, default='Powering production with precision partnerships.')
    hero_title = models.CharField(max_length=200, default='Heavy Machinery, Delivered with Intelligence')
    hero_subtitle = models.TextField(blank=True, default='From turnkey fabrication lines to bespoke automation, we orchestrate the machinery supply chain for world-class manufacturers.')
    primary_cta_label = models.CharField(max_length=80, default='Explore Catalogue')
    primary_cta_link = models.CharField(max_length=200, default='/catalogue/')
    secondary_cta_label = models.CharField(max_length=80, blank=True, default='Request Custom Build')
    secondary_cta_link = models.CharField(max_length=200, blank=True, default='/custom-request/')
    hero_background = models.ImageField(upload_to='hero/', blank=True, null=True)
    about_title = models.CharField(max_length=150, default='Engineering Procurement Reinvented')
    about_body = models.TextField(blank=True)
    experience_highlight = models.CharField(max_length=255, blank=True, default='Global supplier network across 18 countries with ISO-compliant partner factories.')
    experience_years = models.PositiveIntegerField(default=18)
    machines_deployed = models.PositiveIntegerField(default=450)
    uptime_commitment = models.CharField(max_length=120, default='99.2% fleet uptime guarantee')
    response_time = models.CharField(max_length=120, default='Quote turnaround in under 24 hours')
    contact_email = models.EmailField(blank=True)
    contact_phone = models.CharField(max_length=50, blank=True)
    whatsapp_link = models.URLField(blank=True)
    operation_regions = models.CharField(max_length=180, blank=True, help_text='Comma separated list of primary regions served.')
    support_hours = models.CharField(max_length=120, blank=True, default='Global support 24/7')
    newsletter_blurb = models.CharField(max_length=255, blank=True)
    promo_video_url = models.URLField(blank=True)
    footer_statement = models.CharField(max_length=200, blank=True, default='Certified general order supplier serving heavy industry since 2006.')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Site settings'

    def __str__(self):
        return self.business_name or 'Site Settings'


class HeroMetric(models.Model):
    settings = models.ForeignKey(SiteSettings, related_name='metrics', on_delete=models.CASCADE)
    label = models.CharField(max_length=120)
    value = models.CharField(max_length=60)
    icon = models.CharField(max_length=60, blank=True, help_text='Font Awesome icon class, e.g. fa-solid fa-industry')
    display_order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['display_order']

    def __str__(self):
        return f"{self.value} {self.label}"


class ValueProposition(models.Model):
    settings = models.ForeignKey(SiteSettings, related_name='value_props', on_delete=models.CASCADE)
    title = models.CharField(max_length=120)
    description = models.TextField()
    icon = models.CharField(max_length=60, blank=True, help_text='Font Awesome icon class')
    display_order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['display_order']
        verbose_name = 'Value proposition'
        verbose_name_plural = 'Value propositions'

    def __str__(self):
        return self.title


class Industry(models.Model):
    name = models.CharField(max_length=120)
    slug = models.SlugField(unique=True, blank=True)
    description = models.TextField(blank=True)
    icon = models.CharField(max_length=60, blank=True, help_text='Font Awesome icon class')
    feature_statement = models.CharField(max_length=180, blank=True)
    display_order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['display_order', 'name']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class Category(models.Model):
    name = models.CharField(max_length=120)
    slug = models.SlugField(unique=True, blank=True)
    description = models.TextField(blank=True)
    icon = models.CharField(max_length=60, blank=True)
    display_order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['display_order', 'name']
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


def generate_machine_code():
    return f"TNX-{timezone.now().strftime('%Y%m%d')}-{get_random_string(4).upper()}"


class Machine(models.Model):
    AVAILABILITY_CHOICES = [
        ('in_stock', 'In Stock'),
        ('back_order', 'Backorder'),
        ('custom_build', 'Custom Build'),
    ]

    public_id = models.CharField(max_length=20, unique=True, default=generate_machine_code, editable=False)
    name = models.CharField(max_length=150)
    slug = models.SlugField(unique=True, blank=True)
    category = models.ForeignKey(Category, related_name='machines', on_delete=models.CASCADE)
    industries = models.ManyToManyField(Industry, related_name='machines', blank=True)
    short_description = models.CharField(max_length=255)
    description = models.TextField()
    key_features = models.TextField(blank=True, help_text='Use bullet points separated by new lines.')
    model_number = models.CharField(max_length=80, blank=True)
    manufacturer = models.CharField(max_length=120, blank=True)
    power_rating_kw = models.DecimalField(max_digits=7, decimal_places=2, blank=True, null=True, help_text='Kilowatt rating if applicable.')
    capacity_output = models.CharField(max_length=120, blank=True, help_text='e.g. 5,000 bottles/hr or 40 TPH')
    price_from = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)
    currency = models.CharField(max_length=5, default='USD')
    lead_time_weeks = models.PositiveIntegerField(default=8)
    warranty_months = models.PositiveIntegerField(default=12)
    availability_status = models.CharField(max_length=20, choices=AVAILABILITY_CHOICES, default='in_stock')
    highlight_text = models.CharField(max_length=120, blank=True)
    hero_image = models.ImageField(upload_to='machines/hero/', blank=True, null=True)
    brochure = models.FileField(upload_to='machines/brochures/', blank=True, null=True)
    video_url = models.URLField(blank=True)
    is_featured = models.BooleanField(default=False)
    financing_available = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.name)
            slug = base_slug
            counter = 1
            while Machine.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('portal:machine_detail', args=[self.slug])

    @property
    def from_price_display(self):
        if self.price_from is None:
            return 'On Request'
        value = self.price_from
        integral = value == value.to_integral_value()
        amount = f"{value:,.0f}" if integral else f"{value:,.2f}"
        return f"{self.currency} {amount}"


class MachineImage(models.Model):
    machine = models.ForeignKey(Machine, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='machines/gallery/')
    caption = models.CharField(max_length=150, blank=True)
    is_primary = models.BooleanField(default=False)
    display_order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['-is_primary', 'display_order', 'id']

    def __str__(self):
        return f"Image for {self.machine.name}"


class MachineDocument(models.Model):
    machine = models.ForeignKey(Machine, related_name='documents', on_delete=models.CASCADE)
    label = models.CharField(max_length=120)
    document = models.FileField(upload_to='machines/documents/')

    class Meta:
        ordering = ['label']

    def __str__(self):
        return f"{self.label} ({self.machine.name})"


class Partner(models.Model):
    name = models.CharField(max_length=120)
    website = models.URLField(blank=True)
    logo = models.ImageField(upload_to='partners/logos/', blank=True, null=True)
    caption = models.CharField(max_length=160, blank=True)
    display_order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['display_order', 'name']

    def __str__(self):
        return self.name


class Testimonial(models.Model):
    client_name = models.CharField(max_length=120)
    client_role = models.CharField(max_length=120, blank=True)
    company = models.CharField(max_length=120)
    industry = models.ForeignKey(Industry, related_name='testimonials', on_delete=models.SET_NULL, null=True, blank=True)
    quote = models.TextField()
    rating = models.PositiveSmallIntegerField(default=5)
    highlight = models.BooleanField(default=False)
    avatar = models.ImageField(upload_to='testimonials/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-highlight', '-created_at']

    def __str__(self):
        return f"{self.client_name} - {self.company}"


class FAQ(models.Model):
    question = models.CharField(max_length=200)
    answer = models.TextField()
    category = models.CharField(max_length=120, blank=True)
    display_order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['display_order', 'question']
        verbose_name = 'FAQ'
        verbose_name_plural = 'FAQs'

    def __str__(self):
        return self.question


class ServiceOffering(models.Model):
    title = models.CharField(max_length=120)
    description = models.TextField()
    icon = models.CharField(max_length=60, blank=True)
    display_order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['display_order']

    def __str__(self):
        return self.title


def custom_request_reference():
    return f"RQ{timezone.now().strftime('%y%m%d')}" + get_random_string(4).upper()


class CustomRequest(models.Model):
    STATUS_NEW = 'new'
    STATUS_REVIEW = 'review'
    STATUS_QUOTED = 'quoted'
    STATUS_FULFILLED = 'fulfilled'

    STATUS_CHOICES = [
        (STATUS_NEW, 'New'),
        (STATUS_REVIEW, 'Under Review'),
        (STATUS_QUOTED, 'Quoted'),
        (STATUS_FULFILLED, 'Fulfilled'),
    ]

    reference_code = models.CharField(max_length=20, unique=True, default=custom_request_reference, editable=False)
    contact_name = models.CharField(max_length=120)
    company_name = models.CharField(max_length=150)
    email = models.EmailField()
    phone = models.CharField(max_length=50, blank=True)
    industry = models.ForeignKey(Industry, related_name='requests', on_delete=models.SET_NULL, null=True, blank=True)
    machine_type = models.CharField(max_length=180)
    capacity_requirement = models.CharField(max_length=180, blank=True)
    budget_min = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)
    budget_max = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)
    currency = models.CharField(max_length=5, default='USD')
    project_location = models.CharField(max_length=160, blank=True)
    deployment_timeline = models.CharField(max_length=120, blank=True)
    description = models.TextField()
    attachment = models.FileField(upload_to='requests/', blank=True, null=True)
    preferred_contact_method = models.CharField(max_length=80, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=STATUS_NEW)
    internal_notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.reference_code} - {self.company_name}"

    def save(self, *args, **kwargs):
        is_new = self._state.adding
        previous_status = None
        if not is_new:
            previous_status = CustomRequest.objects.filter(pk=self.pk).values_list('status', flat=True).first()
        super().save(*args, **kwargs)
        status_changed = previous_status and previous_status != self.status
        if is_new or status_changed:
            RequestStatusLog.objects.create(custom_request=self, status=self.status, comment='Status updated automatically.')


class RequestStatusLog(models.Model):
    custom_request = models.ForeignKey(CustomRequest, related_name='status_logs', on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=CustomRequest.STATUS_CHOICES)
    comment = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.custom_request.reference_code} -> {self.get_status_display()}"
