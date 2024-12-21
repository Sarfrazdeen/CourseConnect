from django import forms
from .models import contactus, Admission  # Ensure you are importing the Admission model

class ContactForm(forms.ModelForm):
    class Meta:
        model = contactus  # Ensure the model name matches your models.py
        fields = ['Full_name', 'Email', 'Message', 'Phone_number']  # Specify fields to include

    Full_name = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={
            'placeholder': 'Enter your name',
            'class': 'form-control'
        })
    )
    Email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'placeholder': 'Enter your email',
            'class': 'form-control'
        })
    )
    Phone_number = forms.RegexField(
        regex=r'^\+?1?\d{9,15}$',  # Adjust regex as needed
        widget=forms.TextInput(attrs={
            'placeholder': 'Enter your phone number',
            'class': 'form-control'
        }),
        error_messages={
            'invalid': 'Enter a valid phone number (e.g., +123456789).'
        }
    )
    Message = forms.CharField(
        widget=forms.Textarea(attrs={
            'placeholder': 'Enter your message',
            'class': 'form-control',
            'rows': 4
        })
    )

class AdmissionForm(forms.ModelForm):  # Renamed the form class to AdmissionForm
    class Meta:
        model = Admission
        fields = ['full_name', 'email', 'phone', 'course', 'message']  # Fields that should appear in the form

        widgets = {
            'full_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter your full name',
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter your email address',
            }),
            'phone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter your phone number',
            }),
            'course': forms.Select(attrs={
                'class': 'form-select',
            }),
            'message': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Optional: Any additional details or questions',
                'rows': 4,
            }),
        }

        labels = {
            'full_name': 'Full Name',
            'email': 'Email Address',
            'phone': 'Phone Number',
            'course': 'Select Course',
            'message': 'Additional Information',
        }

from django import forms
from .models import Admission

class AdForm(forms.ModelForm):
    class Meta:
        model = Admission
        fields = ['full_name', 'address', 'qualification', 'passed_out', 'passed_out_year',
                  'college_name', 'email', 'phone', 'course', 'message']
        widgets = {
            'message': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Additional Information (optional)'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Add CSS classes to each field
        self.fields['full_name'].widget.attrs.update({'class': 'form-control'})
        self.fields['address'].widget.attrs.update({'class': 'form-control'})
        self.fields['qualification'].widget.attrs.update({'class': 'form-control'})
        self.fields['email'].widget.attrs.update({'class': 'form-control'})
        self.fields['phone'].widget.attrs.update({'class': 'form-control'})
        self.fields['course'].widget.attrs.update({'class': 'form-control'})
        self.fields['message'].widget.attrs.update({'class': 'form-control'})
        
        # Handle the visibility of the 'passed_out_year' field
        if not self.instance or not self.instance.passed_out:
            self.fields['passed_out_year'].required = False
            self.fields['passed_out_year'].widget = forms.HiddenInput()
        else:
            self.fields['passed_out_year'].widget.attrs.update({'class': 'form-control'})


