from django import forms
from storefront.models import ProductConfiguration


class ProductConfigurationForm(forms.ModelForm):
    def __init__(self, size_choices=(), color_choices=(), firmness_choices=(), *args, **kwargs):
        super(ProductConfigurationForm, self).__init__(*args, **kwargs)
        self.fields['size'].choices = size_choices
        self.fields['color'].choices = color_choices
        self.fields['firmness'].choices = firmness_choices

    class Meta:
        model = ProductConfiguration
        fields = ['size', 'color', 'firmness', 'note']


class ProductConfiguratorForm(forms.Form):
    def __init__(self, size_choices=None, color_choices=None, firmness_choices=None, *args, **kwargs):
        super(ProductConfiguratorForm, self).__init__(*args, **kwargs)
        if size_choices:
            self.fields['size'].choices = size_choices
            self.fields['size'].required = True

        if color_choices:
            self.fields['color'].choices = color_choices
            self.fields['color'].required = True

        if firmness_choices:
            self.fields['firmness'].choices = firmness_choices
            self.fields['firmness'].required = True

    size = forms.ChoiceField(choices=(), required=False)
    color = forms.ChoiceField(choices=(), required=False)
    firmness = forms.ChoiceField(choices=(), required=False)
    note = forms.CharField(widget=forms.Textarea, required=False)
