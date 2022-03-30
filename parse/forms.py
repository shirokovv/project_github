from django import forms


class UpdateForm(forms.Form):
    quantity = forms.IntegerField(label='Количество', min_value=1, max_value=100)

    def __init__(self, *args, **kwargs):
        super(UpdateForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'
