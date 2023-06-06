from django import forms


class EmailPostForm(forms.Form):
    name = forms.CharField(max_length=25)
    email = forms.EmailField()
    to = forms.EmailField()
    comments = forms.CharField(required=False, widget=forms.Textarea)

    labels = {
        "name": "Имя",
        "email": "E-mail",
        "to": "Кому",
        "comments": "Комментарий",
    }

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        for label in self.labels:
            self.fields[label].label = self.labels[label]
