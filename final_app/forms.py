# -*- coding: utf-8 -*-
__author__ = 'vladimir.pekarsky'

from django import forms


class SearchPlayerForm(forms.Form):
    email = forms.EmailField(label='Email', required=False)

class ChangeExperienceForm(forms.Form):
    experience = forms.IntegerField(label='Experience', required=False,
                                    min_value=0, max_value=9999)
