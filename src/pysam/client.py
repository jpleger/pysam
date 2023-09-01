#!/usr/bin/env python3
import requests


class SAM:
    _BASE_URL = "https://api.sam.gov/prod/opportunities/v1/search"

    def _get(self, url):
        return requests.get(url, timeout=15).json()
