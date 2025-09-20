from django import forms

from .models import Category, CustomRequest, Industry, Machine


class CustomRequestForm(forms.ModelForm):
    budget_min = forms.DecimalField(required=False, min_value=0, label='Minimum Budget')
    budget_max = forms.DecimalField(required=False, min_value=0, label='Maximum Budget')

    class Meta:
        model = CustomRequest
        fields = [
            'contact_name',
            'company_name',
            'email',
            'phone',
            'industry',
            'machine_type',
            'capacity_requirement',
            'budget_min',
            'budget_max',
            'currency',
            'project_location',
            'deployment_timeline',
            'description',
            'attachment',
            'preferred_contact_method',
        ]
        widgets = {
            'description': forms.Textarea(attrs={'rows': 5, 'placeholder': 'Share duty cycle, utilities, compliance standards, or critical specs.'}),
            'capacity_requirement': forms.TextInput(attrs={'placeholder': 'e.g. 5,000 units/hr or 30 tons per shift'}),
            'deployment_timeline': forms.TextInput(attrs={'placeholder': 'Desired delivery window'}),
            'preferred_contact_method': forms.TextInput(attrs={'placeholder': 'Phone, email, Teams, etc.'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        currency_field = self.fields['currency']
        currency_field.widget = forms.Select(choices=[
            ('USD', 'USD — US Dollar'),
            ('EUR', 'EUR — Euro'),
            ('GBP', 'GBP — British Pound'),
            ('AED', 'AED — UAE Dirham'),
            ('PKR', 'PKR — Pakistani Rupee'),
            ('SAR', 'SAR — Saudi Riyal'),
            ('CNY', 'CNY — Chinese Yuan'),
        ])
        currency_field.initial = currency_field.initial or 'USD'

    def clean(self):
        cleaned_data = super().clean()
        min_budget = cleaned_data.get('budget_min')
        max_budget = cleaned_data.get('budget_max')
        if min_budget and max_budget and min_budget > max_budget:
            self.add_error('budget_max', 'Maximum budget must be greater than or equal to minimum budget.')
        return cleaned_data


class MachineFilterForm(forms.Form):
    search = forms.CharField(required=False, label='Search keyword')
    category = forms.ModelChoiceField(queryset=Category.objects.none(), required=False, empty_label='All categories')
    industry = forms.ModelChoiceField(queryset=Industry.objects.none(), required=False, empty_label='All industries')
    availability = forms.ChoiceField(choices=[('', 'Availability')] + list(Machine.AVAILABILITY_CHOICES), required=False)
    financing = forms.BooleanField(required=False, label='Financing available')
    power_min = forms.DecimalField(required=False, min_value=0, label='Min kW')
    power_max = forms.DecimalField(required=False, min_value=0, label='Max kW')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['category'].queryset = Category.objects.order_by('name')
        self.fields['industry'].queryset = Industry.objects.order_by('name')

    def clean(self):
        cleaned_data = super().clean()
        p_min = cleaned_data.get('power_min')
        p_max = cleaned_data.get('power_max')
        if p_min and p_max and p_min > p_max:
            self.add_error('power_max', 'Max kW must be greater than min kW.')
        return cleaned_data
