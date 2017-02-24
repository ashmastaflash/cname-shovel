import re
from urlparse import urlparse

class Utility(object):
    @classmethod
    def get_urls_from_file(cls, file_name):
        retlist = []
        with open(file_name, 'r') as in_file:
            contents = in_file.readlines()
        for target in contents:
            clean_target = target.rstrip('\n')
            if Utility.is_a_valid_url(clean_target):
                retlist.append(clean_target)
        return retlist

    @classmethod
    def get_urls_from_page_source(cls, page_source):
        all_urls = []
        rx = r'\b((https*://?|www[.])[^\s()<>]+(?:\([\w\d]+\)|([^[:punct:]\s]|/)))'
        for match in re.finditer(rx, page_source):
            if Utility.is_a_valid_url(match.group(0)):
                all_urls.append(match.group(0))
        return all_urls

    @classmethod
    def is_a_valid_url(cls, url):
        valid = True
        try:
            result = urlparse(url)
            if result.scheme not in ["http", "https"]:
                valid = False
            if not result.hostname:
                valid = False
        except Exception as e:
            print "\tEXC %s thrown for URL %s" % (e, url)
            valid = False
        return valid

    
