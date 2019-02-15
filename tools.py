import glob
import re

from main import Downloader
from names import normalize, STDNAMES
from utils import pkl

def download_all():
    journal_files = glob.glob('.papers_*.pkl')
    for jf in journal_files:
        name = re.findall('\.papers_(.*?)\.pkl', jf)[0]
        papers = pkl.load('papers_%s' % name)
        refs = Downloader().download_papers_refs(papers)
        pkl.save(refs, 'refs_%s' % name)

def download_refs(jname, save_every = 100):
    papers = pkl.load('papers_%s' % jname)
    refs = pkl.load('refs_%s' % jname, [])
    existing_uids = {r['by_uid'] for r in refs}
    papers_to_download = [p for p in papers if p['uid'] not in existing_uids]
    print 'downloading %d out of %d papers' % (len(papers_to_download), len(papers))
    d = Downloader()
    for i, chunk in enumerate(chunks(papers_to_download, save_every)):
        print ' -- chunk #%d -- ' % (i + 1)
        refs.extend(d.download_papers_refs(chunk))
        pkl.save(refs, 'refs_%s' % jname)

def update_refs_data(update_func, *args, **kw):
    ref_files = glob.glob('.refs_*.pkl')
    for rf in ref_files:
        name = re.findall('\.(.*?)\.pkl', rf)[0]
        print 'loading %s' % name
        refs = pkl.load(name)
        print 'updating %s' % name
        update_func(refs, *args, **kw)
        print 'saving %s' % name
        pkl.save(refs, name)

def renormalize(refs, full = False):
    def _update(refs, full):
        for r in refs:
            author = r['author']
            r['author'] = normalize(author) if full else STDNAMES.get(author, author)
    update_refs_data(_update, full = full)

def chunks(l, n):
    n = max(1, n)
    return (l[i:i+n] for i in xrange(0, len(l), n))
