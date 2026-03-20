# File: views.py
# Author:Kiefer Ebanks (kebanks@bu.edu), 3/20/2026
# Description: The urls file for the voter_analytics app
# Creating the url paths for the voter_analytics app

from django.db.models.query import QuerySet
from django.shortcuts import render
from django.db.models import Max, Min
from django.views.generic import ListView

from .models import Voter

# Create your views here.

class VoterListView(ListView):
    ''' view to display a list of all voters in the database '''
    model = Voter
    template_name = 'voter_analytics/voters.html' # specify the template to use for this view
    context_object_name = 'voters' # specify the name of the context variable to use in the template to access the list of voters
    paginate_by = 100 # specify 100 voters to be display per page

    def get_queryset(self):
        ''' override the get_queryset method to return a limited queryset of voters'''
        
        voters = super().get_queryset() # get the default queryset of all voters from the database
        
        # look for URL parameters to filter by
        if 'first_name' in self.request.GET: # if the first name parameter is in the URL query string
            first_name = self.request.GET['first_name'].strip() # get the first name parameter from the URL query string
            if first_name: # if the first name parameter is not empty
                voters = voters.filter(first_name=first_name) # filter the queryset by first name

        if 'last_name' in self.request.GET: # if the last name parameter is in the URL query string
            last_name = self.request.GET['last_name'].strip() # get the last name parameter from the URL query string
            if last_name: # if the last name parameter is not empty
                voters = voters.filter(last_name=last_name) # filter the queryset by last name

        if 'party_affiliation' in self.request.GET: # if the party affiliation parameter is in the URL query string
            party = self.request.GET['party_affiliation'].strip() # get the party affiliation parameter from the URL query string
            if party: # if the party affiliation parameter is not empty
                voters = voters.filter(party_affiliation=party) # filter the queryset by party affiliation

        if 'voter_score' in self.request.GET: # if the voter score parameter is in the URL query string
            voter_score = self.request.GET['voter_score'].strip() # get the voter score parameter from the URL query string
            if voter_score: # if the voter score parameter is not empty
                voters = voters.filter(voter_score=int(voter_score)) # filter the queryset by voter score

        if 'dob_min_year' in self.request.GET: # if the dob min year parameter is in the URL query string
            dob_min = self.request.GET['dob_min_year'].strip() # get the dob min year parameter from the URL query string
            if dob_min: # if the dob min year parameter is not empty
                voters = voters.filter(date_of_birth__year__gte=int(dob_min)) # filter the queryset by dob min year greater than or equal to the dob min year parameter

        if 'dob_max_year' in self.request.GET: # if the dob max year parameter is in the URL query string
            dob_max = self.request.GET['dob_max_year'].strip() # get the dob max year parameter from the URL query string
            if dob_max: # if the dob max year parameter is not empty
                voters = voters.filter(date_of_birth__year__lte=int(dob_max)) # filter the queryset by dob max year less than or equal to the dob max year parameter

        if 'voted_in_v20state' in self.request.GET and self.request.GET['voted_in_v20state'] == 'true':
            voters = voters.filter(v20state=True) # filter the queryset by voted in v20state
        if 'voted_in_v21town' in self.request.GET and self.request.GET['voted_in_v21town'] == 'true':
            voters = voters.filter(v21town=True) # filter the queryset by voted in v21town
        if 'voted_in_v21primary' in self.request.GET and self.request.GET['voted_in_v21primary'] == 'true':
            voters = voters.filter(v21primary=True) # filter the queryset by voted in v21primary
        if 'voted_in_v22general' in self.request.GET and self.request.GET['voted_in_v22general'] == 'true':
            voters = voters.filter(v22general=True) # filter the queryset by voted in v22general
        if 'voted_in_v23town' in self.request.GET and self.request.GET['voted_in_v23town'] == 'true':
            voters = voters.filter(v23town=True) # filter the queryset by voted in v23town

        return voters # return the filtered queryset of voters to be displayed in the template

    def get_context_data(self, **kwargs):
        ''' using get_context_data method to add a list of year choices to the context for the search form in the template so I don't have to manually add all the year choices in the template '''
        ctx = super().get_context_data(**kwargs)
        agg = Voter.objects.aggregate( # aggregate the minimum and maximum date of birth from the voters in the database
            min_dob=Min('date_of_birth'),
            max_dob=Max('date_of_birth'),
        )
        min_dob, max_dob = agg['min_dob'], agg['max_dob']
        if min_dob and max_dob:
            y_min, y_max = min_dob.year, max_dob.year
            # create a list of year choices from the minimum year to the maximum year
            # using this for the dropdown menu in the search form in the template
            ctx['year_choices'] = range(y_max, y_min - 1, -1)
        else:
            ctx['year_choices'] = [] # if there are no year choices, set the year choices to an empty list

        g = self.request.GET
        ctx['form_values'] = {
            'first_name': g.get('first_name', ''),
            'last_name': g.get('last_name', ''),
            'party_affiliation': g.get('party_affiliation', ''),
            'dob_min_year': g.get('dob_min_year', ''),
            'dob_max_year': g.get('dob_max_year', ''),
            'voter_score': g.get('voter_score', ''),
            'voted_in_v20state': g.get('voted_in_v20state', ''),
            'voted_in_v21town': g.get('voted_in_v21town', ''),
            'voted_in_v21primary': g.get('voted_in_v21primary', ''),
            'voted_in_v22general': g.get('voted_in_v22general', ''),
            'voted_in_v23town': g.get('voted_in_v23town', ''),
        }

        # Pagination links must repeat the search filters; search.html reads form_values from context
        params = self.request.GET.copy()  # copy so we can edit without changing the real request
        params.pop('page', None)  # strip old page—Next/Previous will append the new page=… once
        
        # urlencode turns the remaining GET params into one piece of text stored as filter_querystring for the template.
        # voters.html pastes that into the Next/Previous href so the URL still carries the filters.
        ctx['filter_querystring'] = params.urlencode()

        return ctx
