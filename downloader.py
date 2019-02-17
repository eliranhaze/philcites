from suds import WebFault
from wos import WosClient

import sys
import time

from names import normalize_author, normalize_title
from parse import parse_journal, parse_ref

class Downloader(object):

    _MIN_REQ_DELAY = .5 # sec
    _BATCH_SIZE = 100

    def __init__(self):
        self._api = WosClient()
        self._last_req_at = 0
        self._connected = False

    def connect(self):
        # must be on a network with access to wos (eg univesity wifi)
        self._log('connecting')
        self._api.connect()
        self._connected = True

    def disconnect(self):
        self._log('disconnecting')
        self._api.close()
        self._connected = False

    def reconnect(self):
        self.disconnect()
        self.connect()

    def download_journal(self, name):
        return self._download(
            download_func = self._api.search,
            download_more_func = self._api.retrieve,
            process_func = self._process_journal,
            query = 'SO=%s' % name,
            count = self._BATCH_SIZE,
        )

    def download_papers_refs(self, papers):
        refs = []
        for i, p in enumerate(papers):
            if p['doctype'].lower() != 'article':
                # skip book reviews, corrections, etc
                continue
            self._log('%d/%d' % (i + 1, len(papers)))
            refs.extend(self.download_refs(p))
        return refs

    def download_refs(self, paper):
        uid = paper['uid']
        self._log('downloading refs for %s' % uid)
        return self._download(
            download_func = self._api.citedReferences,
            download_more_func = self._api.citedReferencesRetrieve,
            process_func = lambda r: self._process_refs(paper, r),
            uid = uid,
        )

    def _download(self, download_func, download_more_func, process_func, *args, **kw):
        result = self._request(download_func, *args, **kw)
        self._log('found %d records' % result.recordsFound)
        parsed = process_func(result)
        offset = self._BATCH_SIZE + 1
        while offset <= result.recordsFound:
            self._log('downloading more (offset=%d)' % offset)
            more = self._request(download_more_func, queryId = result.queryId, offset = offset)
            parsed.extend(process_func(more))
            offset += self._BATCH_SIZE
        return parsed
        
    def _process_journal(self, result):
        papers = parse_journal(result.records)
        self._log('parsed %d papers' % len(papers))
        return papers

    def _process_refs(self, paper, result):
        refs = []
        if type(result) == list:
            # when downloading using citedReferencesRetrieve function - thanks WoS for inconsistent formats
            result_refs = result
        else:
            # when downloading using citedReferences
            result_refs = getattr(result, 'references', [])
        for ref in result_refs:
            ref = parse_ref(ref)
            ref['by_uid'] = paper['uid']
            ref['by_year'] = paper['year']
            ref['author'] = normalize_author(ref['author'])
            ref['title'] = normalize_title(ref['author'])
            refs.append(ref)
        return refs

    def _request(self, func, *args, **kw):
        if not self._connected:
            self.connect()
        attempt = 1
        while True:
            try:
                self._throttle()
                self._last_req_at = time.time()
                return func(*args, **kw)
            except WebFault:
                self._log('got web fault')
                if attempt >= 3:
                    self.reconnect()
                if attempt == 6:
                    raise
                time.sleep(attempt ** 2)
                attempt += 1
                self._log('retrying')

    def _throttle(self):
        next_req_at = self._last_req_at + self._MIN_REQ_DELAY
        until_allowed = next_req_at - time.time()
        if until_allowed > 0:
            self._log('throttling %.2fs' % until_allowed)
            time.sleep(until_allowed)

    def _log(self, msg):
        print msg
