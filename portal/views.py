from django.conf import settings
from django.contrib import messages
from django.core.mail import send_mail
from django.db.models import Q
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import DetailView, ListView, TemplateView
from django.views.generic.edit import FormView

from .forms import CustomRequestForm, MachineFilterForm
from .models import (
    Category,
    CustomRequest,
    FAQ,
    Industry,
    Machine,
    Partner,
    ServiceOffering,
    SiteSettings,
    Testimonial,
)


class LandingPageView(TemplateView):
    template_name = 'portal/landing.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        settings_obj = SiteSettings.load()
        context['settings'] = settings_obj
        context['metrics'] = settings_obj.metrics.all()
        context['value_props'] = settings_obj.value_props.all()
        context['industries'] = Industry.objects.all()
        context['services'] = ServiceOffering.objects.all()
        context['featured_machines'] = (
            Machine.objects.filter(is_featured=True)
            .select_related('category')
            .prefetch_related('industries', 'images')[:6]
        )
        context['testimonials'] = Testimonial.objects.all()[:6]
        context['partners'] = Partner.objects.all()
        context['faqs'] = FAQ.objects.all()
        context['custom_request_form'] = CustomRequestForm()
        context['catalogue_url'] = reverse_lazy('portal:machine_list')
        return context


class MachineListView(ListView):
    model = Machine
    template_name = 'portal/machine_list.html'
    context_object_name = 'machines'
    paginate_by = 9

    def get_queryset(self):
        queryset = (
            Machine.objects.all()
            .select_related('category')
            .prefetch_related('industries')
        )
        form = self.filter_form
        if form.is_valid():
            data = form.cleaned_data
            if data.get('search'):
                query = data['search']
                queryset = queryset.filter(
                    Q(name__icontains=query)
                    | Q(short_description__icontains=query)
                    | Q(model_number__icontains=query)
                    | Q(manufacturer__icontains=query)
                    | Q(description__icontains=query)
                )
            if data.get('category'):
                queryset = queryset.filter(category=data['category'])
            if data.get('industry'):
                queryset = queryset.filter(industries=data['industry'])
            if data.get('availability'):
                queryset = queryset.filter(availability_status=data['availability'])
            if data.get('financing'):
                queryset = queryset.filter(financing_available=True)
            p_min = data.get('power_min')
            p_max = data.get('power_max')
            if p_min is not None:
                queryset = queryset.filter(power_rating_kw__gte=p_min)
            if p_max is not None:
                queryset = queryset.filter(power_rating_kw__lte=p_max)
        return queryset.order_by('-is_featured', 'name')

    @property
    def filter_form(self):
        if not hasattr(self, '_filter_form'):
            self._filter_form = MachineFilterForm(self.request.GET or None)
        return self._filter_form

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter_form'] = self.filter_form
        context['settings'] = SiteSettings.load()
        context['custom_request_form'] = CustomRequestForm()
        querydict = self.request.GET.copy()
        querydict.pop('page', None)
        context['querystring'] = querydict.urlencode()
        return context


class MachineDetailView(DetailView):
    model = Machine
    template_name = 'portal/machine_detail.html'
    context_object_name = 'machine'
    slug_field = 'slug'
    slug_url_kwarg = 'slug'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['related_machines'] = (
            Machine.objects.exclude(pk=self.object.pk)
            .filter(category=self.object.category)
            .prefetch_related('industries')[:4]
        )
        context['settings'] = SiteSettings.load()
        context['custom_request_form'] = CustomRequestForm(initial={'machine_type': self.object.name})
        return context


class CustomRequestCreateView(FormView):
    template_name = 'portal/custom_request_form.html'
    form_class = CustomRequestForm
    success_url = reverse_lazy('portal:request_thanks')

    def form_valid(self, form):
        custom_request = form.save()
        self.send_notification(custom_request)
        messages.success(self.request, 'Thank you! Our procurement strategists will respond within 24 hours.')
        return super().form_valid(form)

    def send_notification(self, custom_request: CustomRequest):
        subject = f"New custom machinery request: {custom_request.reference_code}"
        lines = [
            f"Request Reference: {custom_request.reference_code}",
            f"Company: {custom_request.company_name}",
            f"Contact: {custom_request.contact_name} ({custom_request.email})",
            f"Machine Type: {custom_request.machine_type}",
            f"Budget: {custom_request.currency} {custom_request.budget_min or '—'} - {custom_request.budget_max or '—'}",
            '',
            f"Project Location: {custom_request.project_location or 'Provided on follow-up'}",
            f"Timeline: {custom_request.deployment_timeline or 'Provided on follow-up'}",
            '',
            'Description:',
            custom_request.description,
        ]
        message = "\n".join(lines)
        recipient = settings.CONTACT_EMAIL
        if recipient:
            try:
                send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [recipient], fail_silently=True)
            except Exception:
                pass



class RequestThankYouView(TemplateView):
    template_name = 'portal/request_thanks.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['settings'] = SiteSettings.load()
        return context


class LandingRequestView(CustomRequestCreateView):
    http_method_names = ['post']

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, 'Request received! Expect a curated shortlist shortly.')
        return redirect('portal:landing')

    def form_invalid(self, form):
        messages.error(self.request, 'Please check the form and provide the required information to proceed.')
        return redirect('portal:landing')
