#!/usr/bin/env python3
from datetime import datetime, timedelta

import requests


class SAM:
    _SEARCH_URL = "https://api.sam.gov/prod/opportunities/v1/search"
    _TIME_FORMAT = '%m/%d/%Y'
    _PROCUREMENT_TYPES = {
        'u': 'Justification and Approval (J&A)',
        'p': 'Presolicitation',
        'a': 'Award Notice',
        'r': 'Sources Sought',
        's': 'Special Notice',
        'o': 'Solicitation',
        'g': 'Sale of Surplus Property',
        'k': 'Combined Synopsis/Solicitation',
        'i': 'Intent to Bundle Requirements',
        'f': 'Foreign Government Standard',
        'l': 'Fair Opportunity / Limited Sources Justification',
    }

    def get_all_opportunities(self, start_date=None, end_date=None):
        # If there is no end_date, set it to today
        if not end_date:
            end_date = datetime.today().strftime(self._TIME_FORMAT)
        # If there is no start_date, set it to yesterday
        if not start_date:
            start_date = (datetime.today() - timedelta(days=1)).strftime(self._TIME_FORMAT)
        return self.search_opportunities(start_date, end_date)

    def search_opportunities(
        self,
        start_date,
        end_date,
        limit=1000,
        procurement_type=None,
        solicitation_number=None,
        notice_id=None,
        title=None,
        department_name=None,
        agency_name=None,
        place_of_performance_state=None,
        place_of_performance_zip=None,
        org_code=None,
        org_name=None,
        set_aside=None,
        set_aside_description=None,
        naics_code=None,
        classification_code=None,
        response_deadline_start=None,
        response_deadline_end=None,
    ):
        """
        Search for opportunities on sam.gov.
        """
        # Validate input

        # Check for valid dates in start_date, end_date, response_deadline_start, and response_deadline_end.
        for date in [start_date, end_date, response_deadline_start, response_deadline_end]:
            if date:
                if not isinstance(date, datetime):
                    msg = f"Invalid date type: {date}, should be a datetime object."
                    raise ValueError(msg)
        # Check for valid procurement_type.
        if procurement_type:
            if not isinstance(procurement_type, str) and procurement_type not in self._PROCUREMENT_TYPES.keys():
                msg = f"Invalid procurement_type: {procurement_type}. Please use a valid procurement_type."
                raise ValueError(msg)
        # Check for valid state.
        if place_of_performance_state:
            if not isinstance(place_of_performance_state, str) and len(place_of_performance_state) != 2:
                msg = f"Invalid state: {place_of_performance_state}. Please use a valid state abbreviation."
                raise ValueError(msg)
        # Check for valid zip code.
        if place_of_performance_zip:
            if not isinstance(place_of_performance_zip, str) and len(place_of_performance_zip) != 5:
                msg = f"Invalid zip code: {place_of_performance_zip}. Please use a valid zip code."
                raise ValueError(msg)
        # Check to see that the limit is not greater than 1000 or smaller than 0.
        if limit > 1000 or limit < 0:
            msg = f"Invalid limit: {limit}. Please use a limit between 0 and 1000."
            raise ValueError(msg)

        # Verify that date range for start_date and end_date is within 1 year.
        if (end_date - start_date).days > 365:
            msg = f"Invalid date range: {start_date} to {end_date}. Please use a date range within 1 year."
            raise ValueError(msg)

        # Build the query parameters
        query_params = {
            'postedFrom': start_date.strftime(self._TIME_FORMAT),
            'postedTo': end_date.strftime(self._TIME_FORMAT),
            'limit': limit,
            'offset': 0,
        }
        if response_deadline_end:
            query_params['rdlto'] = response_deadline_end.strftime(self._TIME_FORMAT)
        if response_deadline_start:
            query_params['rdlfrom'] = response_deadline_start.strftime(self._TIME_FORMAT)
        param_mapping = {
            'ptype': procurement_type,
            'solnum': solicitation_number,
            'noticeid': notice_id,
            'title': title,
            'deptname': department_name,
            'subtier': agency_name,
            'state': place_of_performance_state,
            'zip': place_of_performance_zip,
            'organizationCode': org_code,
            'organizationName': org_name,
            'typeOfSetAside': set_aside,
            'typeOfSetAsideDescription': set_aside_description,
            'ncode': naics_code,
            'ccode': classification_code,
        }
        for param, value in param_mapping.items():
            if value:
                query_params[param] = value
        results_raw = []
        results = []
        # Gather the results
        while True:
            response = requests.get(self._SEARCH_URL, params=query_params, timeout=120)
            response_json = response.json()
            # If there are less records than the limit, we can break from the loop
            if response_json['totalRecords'] != limit or response_json['totalRecords'] != 1000:
                break
            results_raw.append(response_json)
            query_params['offset'] += limit
        # Parse the results, returning a pythonic representation of the data

        # Return the results
        return results
