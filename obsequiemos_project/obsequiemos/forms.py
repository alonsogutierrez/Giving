from datetime import date
from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator, MaxValueValidator, MinValueValidator
from django.forms.extras.widgets import SelectDateWidget
from obsequiemos.models import Gift, UserProfile, Post, Picture, Comment, DispatchMethod, CategoryGift, SubcategoryGift, \
    GiftDimensionType, GiftStateType, UsedTimeType, RegionPost, ProvinciaPost, ComunaPost, Postulations, GiftWeightType


class UserForm(forms.ModelForm):
    username = forms.CharField(label='Nombre usuario',
                               min_length=5,
                               widget=forms.TextInput,
                               )
    email = forms.CharField(label='Email',
                            widget=forms.TextInput,
                            )

    first_name = forms.CharField(label='Nombre',
                                 min_length=5,
                                 widget=forms.TextInput,
                                 )

    last_name = forms.CharField(label='Apellido',
                                 min_length=5,
                                 widget=forms.TextInput,
                                 )
    password = forms.CharField(widget=forms.PasswordInput())


    class Meta:
        model = User
        fields = ('username','email','first_name','last_name','password',)

class UserProfileForm(forms.ModelForm):

    phone_regex = RegexValidator(regex=r'^\+?1?\d{8,15}$',
                                 message="El numero ingresado no es del formato: '+999999999' o no esta entre 9 y 15 digitos.")

    phone = forms.CharField(validators=[phone_regex], label='Telefono', required=True)

    address = forms.CharField(label='Direccion',
                              min_length=5,
                              widget=forms.TextInput,
                              required=False,
                              )


    class Meta:
        model = UserProfile
        fields = ('phone', 'address')


class PasswordForm(forms.Form):
    password = forms.CharField(widget=forms.PasswordInput, required=False)
    confirm_password = forms.CharField(widget=forms.PasswordInput, required=False)
    current_password = forms.CharField(widget=forms.PasswordInput, required=False)

    def __init__(self, user, *args, **kwargs):
        self.user = user
        super(PasswordForm, self).__init__(*args, **kwargs)

    def clean_current_password(self):
        # If the user entered the current password, make sure it's right
        if self.cleaned_data['current_password'] and not self.user.check_password(
                self.cleaned_data['current_password']):
            raise ValidationError('This is not your current password. Please try again.')

        # If the user entered the current password, make sure they entered the new passwords as well
        if self.cleaned_data['current_password'] and not (
            self.cleaned_data['password'] or self.cleaned_data['confirm_password']):
            raise ValidationError('Please enter a new password and a confirmation to update.')

        return self.cleaned_data['current_password']

    def clean_confirm_password(self):
        # Make sure the new password and confirmation match
        password1 = self.cleaned_data.get('password')
        password2 = self.cleaned_data.get('confirm_password')

        if password1 != password2:
            raise forms.ValidationError("Your passwords didn't match. Please try again.")

        return self.cleaned_data.get('confirm_password')

    class Meta:
        model = User
        fields = ('password', 'confirm_password', 'current_password',)

class PostForm(forms.ModelForm):

    title = forms.CharField(label='Titulo',
                            min_length=5,
                            widget=forms.TextInput,
                            )

    detail = forms.CharField(label='Motivo',
                            min_length=15,
                            widget=forms.Textarea,
                            )

    finish_date = forms.DateField(label='Fecha termino',
                                  initial=date.today,
                                  widget=SelectDateWidget,
                                  )

    region = forms.ModelChoiceField(label='Region',
                                    queryset=RegionPost.objects.all().order_by('region_name'),
                                    to_field_name="region_name",
                                    )
    provincia = forms.ModelChoiceField(required=False,
                                       label='Provincia',
                                       queryset=ProvinciaPost.objects.all().order_by('provincia_name'),
                                       to_field_name="provincia_name",
                                       )
    comuna = forms.ModelChoiceField(  # required=False,
        # label='Comuna',
        queryset=None,
        # to_field_name="comuna_name",
    )
    person2person_dispatch = forms.BooleanField(initial=False, required=False)
    pay_winner_dispatch = forms.BooleanField(initial=False, required=False)
    giver_pay_dispatch = forms.BooleanField(initial=False, required=False)
    according_to_winner_dispatch = forms.BooleanField(initial=False, required=False)

    def __init__(self, *args, **kwargs):
        super(PostForm, self).__init__(*args, **kwargs)
        self.fields['comuna'].queryset = ComunaPost.objects.all()

    class Meta:
        model = Post

        fields = ('title','detail','finish_date',
                  'region',
                  'provincia',
                  'comuna',
                  'person2person_dispatch',
                  'pay_winner_dispatch',
                  'giver_pay_dispatch',
                  'according_to_winner_dispatch',
                  )


class GiftForm(forms.ModelForm):
    name = forms.CharField(label='Nombre',
                            min_length=5,
                            widget=forms.TextInput,
                            )
    category = forms.ModelChoiceField(label='Categoria',
                                       queryset=CategoryGift.objects.all(),
                                      to_field_name="name_category",
                                      )
    subcategory = forms.ModelChoiceField(#label='Subcategoria',
        # to_field_name="name_subcategory",
        queryset=None,
    )
    used_time_type = forms.ModelChoiceField(label='Formato de uso',
                                            queryset=UsedTimeType.objects.all(),
                                            to_field_name="time_type",
                                             )
    dimension_type = forms.ModelChoiceField(label='Formato dimensiones',
                                             queryset=GiftDimensionType.objects.all(),
                                            to_field_name="dimension_type",
                                             )
    state_type = forms.ModelChoiceField(label='Estado',
                                             queryset=GiftStateType.objects.all(),
                                        to_field_name="state_type",
                                             )
    length = forms.DecimalField(label='Largo',
                                widget=forms.NumberInput,
                                )
    height = forms.DecimalField(label='Alto',
                                widget=forms.NumberInput,
                                )
    width = forms.DecimalField(label='Ancho',
                               widget=forms.NumberInput,
                               )
    type_weight = forms.ModelChoiceField(label='Unidad de peso',
                                         required=True,
                                         queryset=GiftWeightType.objects.all(),
                                         to_field_name="weight_type",
                                         )
    weight = forms.DecimalField(label='Peso',
                                widget=forms.NumberInput,
                                )
    cant_used_time = forms.DecimalField(label='Tiempo usado',
                                        widget=forms.NumberInput,
                                        )

    def __init__(self, *args, **kwargs):
        super(GiftForm, self).__init__(*args, **kwargs)
        self.fields['subcategory'].queryset = SubcategoryGift.objects.all()

    class Meta:
        model = Gift
        fields = ('name', 'category', 'used_time_type', 'dimension_type', 'state_type', 'length',
                  'height', 'width','type_weight', 'weight', 'cant_used_time')


class PictureForm(forms.ModelForm):
    class Meta:
        model = Picture
        fields = ('picture',)

class CommentForm(forms.ModelForm):

    text = forms.CharField(label='',
                           min_length=5,
                           widget=forms.Textarea,
                           )

    class Meta:
        model = Comment
        fields = ('text',)

class PostulationForm(forms.ModelForm):

    reason = forms.CharField(label='Motivo',
                            min_length=5,
                            widget=forms.Textarea,
                            )

    class Meta:
        model = Postulations
        fields = ('reason',)

class EvaluationForm(forms.ModelForm):

    avg_reputation = forms.IntegerField(
        label='Promedio reputacion',
        widget=forms.NumberInput,
        validators=[
            MaxValueValidator(5),
            MinValueValidator(0)
        ]
    )

    class Meta:
        model = UserProfile
        fields = ('avg_reputation',)
