from bs4 import BeautifulSoup as bs

def parse_journal(journal_xml):
    results = []
    soup = bs(journal_xml, 'xml')
    records = soup.find_all('REC')
    for rec in records:
        uid = rec.find('UID').text
        try:
            journal = rec.find('title', attrs={'type':'source'}).text
            doctype = rec.find('doctype').text
            title = rec.find('title', attrs={'type':'item'}).text
            author = rec.find('name', attrs={'role':'author'}).find('full_name').text
            year = rec.find('pub_info').attrs['pubyear']
            results.append(dict(
                uid = uid,
                journal = journal,
                doctype = doctype,
                title = title,
                author = author,
                year = year,
            ))
        except:
            print 'failed to parse %s' % uid
    return results

def parse_ref(ref):
    return dict(
        author = getattr(ref, 'citedAuthor', ''),
        year = getattr(ref, 'year', ''),
        title = getattr(ref, 'citedWork', '')  + ' - ' + getattr(ref, 'citedTitle', ''),
    )
