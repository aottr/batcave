from django import forms
from django.core.exceptions import ValidationError
from storefront.models import ProductConfiguration


class ProductConfigurationForm(forms.ModelForm):

    amount = forms.IntegerField(min_value=1, step_size=1, initial=1)
    amount.widget.attrs['class'] = 'input input-bordered max-w-xs'

    def clean(self):
        cleaned_data = super(ProductConfigurationForm, self).clean()
        if not self.product:
            raise ValidationError("Product not found.")
        if not self.user:
            raise ValidationError("User is not logged in.")

        return cleaned_data

    def clean_amount(self):
        amount = self.cleaned_data["amount"]

        if amount > self.product.stock:
            raise ValidationError("We don't have enough in stock.")

        # Always return a value to use as the new cleaned data, even if
        # this method didn't change it.
        return amount

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        self.product = kwargs.pop('product', None)
        size_choices = kwargs.pop('size_choices', ())
        color_choices = kwargs.pop('color_choices', ())
        firmness_choices = kwargs.pop('firmness_choices', ())
        super(ProductConfigurationForm, self).__init__(*args, **kwargs)
        # has to be done this way, otherwise BaseModelForms complains about kwargs

        if size_choices:
            self.fields['size'].choices = size_choices
            self.fields['size'].widget.attrs['class'] = 'select select-bordered w-full'
        else:
            del self.fields['size']
        if color_choices:
            self.fields['color'].choices = color_choices
            self.fields['color'].widget.attrs['class'] = 'select select-bordered w-full'
        else:
            del self.fields['color']
        if firmness_choices:
            self.fields['firmness'].choices = firmness_choices
            self.fields['firmness'].widget.attrs['class'] = 'select select-bordered w-full'
        else:
            del self.fields['firmness']

        self.fields['note'].widget.attrs = {
            'class': 'textarea textarea-bordered w-full',
            'placeholder': 'Bi-Color with blue and yellow...'
        }

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
