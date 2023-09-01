# pysam

SAM.gov is a system for viewing opportunities with the federal government. Most government contracts will be published on this site and pysam is a python library for interacting with this data.

## Installation

Installation of pysam is quite simple, using `pip`, just install the package:

```
$ pip3 install pysam
```

## Usage

Export your SAM API key as an environment variable:

```
export SAM_API_KEY=YOUR_API_KEY
```

Then you can use the library to query the API:

```python
from pysam import SAM
client = SAM()
client.search('NAICS', '541511')
```
