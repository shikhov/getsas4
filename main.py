import logging
import urllib2
import multipart
import re
import json
from distutils.version import LooseVersion

from google.appengine.ext import ndb
import webapp2
from config import TGTOKEN, TGCHATID, GAPIKEY, GFOLDERID

TGAPIURL = 'https://api.telegram.org/bot' + TGTOKEN + '/'
GAPIURL = 'https://www.googleapis.com/drive/v3/'

class LastVersion(ndb.Model):
    version = ndb.StringProperty()

class getsas4(webapp2.RequestHandler):
    def get(self):
        url = GAPIURL + "files?q='" + GFOLDERID + "'+in+parents&key=" + GAPIKEY
        jsonResponse = json.loads(urllib2.urlopen(url).read())
        version = ''

        for gfile in jsonResponse.get('files', []):
            rg = re.search(r'(SAS4Android-([\d.]+).*)\.apk', gfile['name'])
            if rg:
                version = rg.group(1).encode('ascii')
                release = rg.group(2).encode('ascii')
                fileid = gfile['id']
                lastversion = LastVersion.get_by_id('version')

                if LooseVersion(release) > LooseVersion(lastversion.version):
                    logging.warn('New version! ' + version)
                    lastversion.version = release
                    lastversion.put()
                    dfile = urllib2.urlopen('https://drive.google.com/uc?id='+fileid).read()
                    if len(dfile) > 500000:
                        multipart.post_multipart(TGAPIURL + 'sendDocument', [(
                            'chat_id', TGCHATID), ('caption', release)], [('document', version+'.apk', dfile)])
                    else:
                        logging.error('Invalid file')
                else:
                    logging.info('No new version (' + version + ')')

        if version == '':
            logging.error('No files matched regexp')

app = webapp2.WSGIApplication([
    ('/getsas4', getsas4),
])
