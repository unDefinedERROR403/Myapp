from django import forms
from myapp.models import Order, Client


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['client', 'product', 'num_units']
        widgets = {'client': forms.RadioSelect()}
        labels = {
            'num_units': 'Quantity',
            'client': 'Client Name',
        }


class InterestForm(forms.Form):
    interested = forms.ChoiceField(choices=[(1, 'Yes'), (0, 'No')], widget=forms.RadioSelect)
    quantity = forms.IntegerField(min_value=1)
    comments = forms.CharField(required=False, widget=forms.Textarea, label='Additional Comments')


class NewUserForm(forms.ModelForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = Client
        fields = ('username', 'email', 'first_name', 'last_name', 'password')

    def save(self, commit=True):
        user = super(NewUserForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user
