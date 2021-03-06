from collections import OrderedDict
from django.contrib import admin

from django.conf.urls import patterns
from django.shortcuts import render_to_response

class ParticipantAdmin(admin.ModelAdmin):

    def link(self, instance):
        url = instance.start_url()
        return '<a href="{}" target="_blank">{}</a>'.format(url, 'Link')

    link.short_description = "Participant link"
    link.allow_tags = True
    list_filter = ['match', 'treatment', 'experiment']

class MatchAdmin(admin.ModelAdmin):
    list_filter = ['treatment', 'experiment']

class TreatmentAdmin(admin.ModelAdmin):
    def link(self, instance):
        url = instance.start_url()
        return '<a href="{}" target="_blank">{}</a>'.format(url, 'Link')

    link.short_description = "Demo link"
    link.allow_tags = True
    list_filter = ['experiment']

class ExperimentAdmin(admin.ModelAdmin):
    def mturk_link(self, instance):
        url = instance.mturk_start_url()
        return '<a href="{}" target="_blank">{}</a>'.format(url, 'Link')

    mturk_link.short_description = "MTurk link (requires workerId to be appended to URL with JavaScript)"
    mturk_link.allow_tags = True

    def payments_link(self, instance):
        return '<a href="{}" target="_blank">{}</a>'.format('{}/payments/'.format(instance.pk), 'Link')

    payments_link.short_description = "Payments page"
    payments_link.allow_tags = True


    def experimenter_input_link(self, instance):
        url = instance.experimenter_input_url()
        return '<a href="{}" target="_blank">{}</a>'.format(url, 'Link')

    experimenter_input_link.short_description = 'Link for experimenter input during gameplay'
    experimenter_input_link.allow_tags = True

    def get_urls(self):
        urls = super(ExperimentAdmin, self).get_urls()
        my_urls = patterns('',
            (r'^(?P<pk>\d+)/payments/$', self.admin_site.admin_view(self.payments))
        )
        return my_urls + urls

    def payments(self, request, pk):
        experiment = self.model.objects.get(pk=pk)
        participants = experiment.participants()
        return render_to_response('admin/Payments.html',
                                  {'participants': participants,
                                   'total_payments': sum(p.total_pay() for p in participants if p.total_pay())})


def remove_duplicates(lst):
    return list(OrderedDict.fromkeys(lst))

def get_list_display(ModelName, readonly_fields, first_fields):
    all_field_names = [field.name for field in ModelName._meta.fields]

    # make sure they're actually in the model.
    first_fields = [f for f in first_fields if f in all_field_names]

    list_display = first_fields + readonly_fields + all_field_names
    return remove_duplicates(list_display)

def get_readonly_fields(fields_common_to_all_models, fields_specific_to_this_subclass):
    return remove_duplicates(fields_common_to_all_models + fields_specific_to_this_subclass)

def get_participant_readonly_fields(fields_specific_to_this_subclass):
    return get_readonly_fields(['link', 'bonus_display'], fields_specific_to_this_subclass)

def get_participant_list_display(Participant, readonly_fields, first_fields=None):
    first_fields = ['__unicode__', 'id', 'experiment', 'treatment', 'match', 'has_visited'] + (first_fields or [])
    return get_list_display(Participant, readonly_fields, first_fields)

def get_match_readonly_fields(fields_specific_to_this_subclass):
    return get_readonly_fields([], fields_specific_to_this_subclass)

def get_match_list_display(Match, readonly_fields, first_fields=None):
    first_fields = ['__unicode__', 'id', 'experiment', 'treatment', 'time_started'] + (first_fields or [])
    return get_list_display(Match, readonly_fields, first_fields)

def get_treatment_readonly_fields(fields_specific_to_this_subclass):
    return get_readonly_fields(['link'], fields_specific_to_this_subclass)

def get_treatment_list_display(Treatment, readonly_fields, first_fields=None):
    first_fields = ['__unicode__', 'id', 'description', 'experiment'] + (first_fields or [])
    return get_list_display(Treatment, readonly_fields, first_fields)

def get_experiment_readonly_fields(fields_specific_to_this_subclass):
    return get_readonly_fields(['mturk_link', 'experimenter_input_link', 'payments_link'], fields_specific_to_this_subclass)

def get_experiment_list_display(Experiment, readonly_fields, first_fields=None):
    first_fields = ['__unicode__', 'id', 'description'] + (first_fields or [])
    return get_list_display(Experiment, readonly_fields, first_fields)
