# encoding: utf-8

"""
Client for read access to the Offenes Köln API.

Author: Marian Steinbach
Website: https://github.com/marians/ok-python-client
License: Public Domain
"""

import urllib
import urllib2
import json
from datetime import datetime
from sets import Set


class Document(object):
    """
    Represents a document
    """
    reference = None
    raw_data = None
    date = None
    title = None
    attachments = None

    def __init__(self, data):
        self.raw_data = data
        self.reference = data['reference']
        self.date = datetime.strptime(data['date'][0], '%Y-%m-%d')
        self.title = data['title'][0]
        if 'attachments' in data and data['attachments'] is not None:
            self.attachments = []
            for att in data['attachments']:
                self.attachments.append(Attachment(att))

    def __repr__(self):
        return '<OKDocument "%s">' % self.reference

    def __str__(self):
        return json.dumps(self.raw_data, indent=4)

    def __getattr__(self, attr):
        return self.raw_data[attr]


class Attachment(object):

    raw_data = None
    last_modified = None
    thumbnails = None

    # TODO: make individual thumbnail accessible by
    #       page number and height

    def __init__(self, data):
        self.raw_data = data
        if 'last_modified' in data and data['last_modified'] is not None:
            self.last_modified = datetime.strptime(
                data['last_modified'], '%Y-%m-%dT%H:%M:%SZ')
        if 'thumbnails' in data and data['thumbnails'] is not None:
            self.thumbnails = []
            for t in data['thumbnails']:
                self.thumbnails.append(Thumbnail(t))

    def __getattr__(self, attr):
        return self.raw_data[attr]


class Thumbnail(object):

    raw_data = None

    def __init__(self, data):
        self.raw_data = data

    def __getattr__(self, attr):
        return self.raw_data[attr]


class Response(object):
    """
    Handler for an API method response
    """
    status = None
    request_duration = None
    request_params = None
    hits = None
    result_entries = None
    max_score = None
    start = None
    method = None

    def __init__(self, response_dict, method):
        """
        Turn a returned dict (from JSON) to a
        more convenient object

        Parameters:
        response_dict: Response dict
        method: Name of the method that has been called
        """
        if response_dict is None:
            raise ValueError("Argument 'response_dict' is None")
        if method is None:
            raise ValueError("Argument 'method' is None")
        self.method = method
        self.status = response_dict['status']
        self.request_duration = response_dict['duration']
        self.request_params = response_dict['request']

    def okay(self):
        """
        Return true if the response is all right.
        """
        if self.status == 0:
            return True
        return False

    def __iter__(self):
        for entry in self.result_entries:
            yield entry

    def __getitem__(self, index):
        return self.result_entries[index]

    def __len__(self):
        if self.result_entries is not None:
            return len(self.result_entries)
        return None

    def __eq__(self, other):
        """Determine if two responses are equal"""
        if self.request_params != other.request_params:
            return False
        if self.status != other.status:
            return False
        if self.hits != other.hits:
            return False
        return True


class DocumentsResponse(Response):
    def __init__(self, response_dict):
        super(DocumentsResponse,
              self).__init__(response_dict, 'documents')
        if ('response' in response_dict and
            response_dict['response'] is not None):
            if 'numhits' in response_dict['response']:
                self.hits = response_dict['response']['numhits']
            if 'maxscore' in response_dict['response']:
                self.max_score = response_dict['response']['maxscore']
            if 'start' in response_dict['response']:
                self.start = response_dict['response']['start']
            self.result_entries = []
            for doc in response_dict['response']['documents']:
                self.result_entries.append(Document(doc))

    def has_next_page(self):
        """
        Returns true if there is a next chunk for this result.
        This only works for "documents" responses.
        """
        if self.hits is not None and self.start is not None:
            rest = self.hits - self.start - len(self.result_entries)
            if rest > 0:
                return True
        return False


class Client(object):

    baseurl = 'http://offeneskoeln.de/api/'

    def documents(self,
                  reference=None,
                  query=None,
                  filter_query=None,
                  limit=10,
                  start=0,
                  sort=None,
                  date_start=None,
                  date_end=None,
                  attachments=False,
                  thumbnails=False,
                  consultations=False,
                  facets=False):
        """
        Retrieve documents (or a specific single document) from
        the database.

        You can directly refer to a specific document using the
        reference parameter. In this case, you are in "direct retrieval"
        mode and arguments start, sort, daterange and limit have no effect.

        Otherwise (when not using the reference argument) you are in
        search mode. This means you can use the following parameters
        to narrow down your search:

        query: Lucene-style query string
        filter_query: Lucene-style filter query string
        limit: Number of documents to return (max: 100)
        start: Result list offset
        sort: Sort order. Defaults to "score desc"
        date_start: Start date of the special date range filter
        date_end: End date of the special date range filter
        """
        output = Set([])
        if attachments:
            output.add('attachments')
        if thumbnails:
            output.add('attachments')
            output.add('thumbnails')
        if consultations:
            output.add('consultations')
        if facets:
            output.add('facets')
        # gather method parameters
        params = {}
        if reference is not None:
            params['reference'] = reference
        if len(output):
            params['output'] = ','.join(output)
        return self.call_method('documents', params)

    def locations(self):
        pass

    def streets(self):
        pass

    def terms(self):
        pass

    def call_method(self, method, params=None):
        """
        Sends the method call to the server. Arguments:
        method: String identifying the method on the server, e.g. "documents"
        params: Optional dict or key-value-tuples with method parameters
        """
        url = self.baseurl + method
        if params is not None and params != {}:
            qs = urllib.urlencode(params)
            url += '?' + qs
        request = urllib2.urlopen(url)
        response = request.read()
        if method == 'documents':
            return DocumentsResponse(json.loads(response))
        else:
            # TODO: instanciate specific response types as implemented
            return Response(json.loads(response), method)


