import gzip
import json

import urllib2

import requests

from joblib import Parallel, delayed

import sys


#opener = urllib2.build_opener()
#opener.addheaders = [('User-Agent', 'Mozilla/5.0')]

GLOBAL_TIMEOUT=10
headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2227.1 Safari/537.36'}
GLOBAL_REQUEST_SESSION = requests.Session()
GLOBAL_REQUEST_SESSION.headers.update(headers)

def get_url(x):
    try:
        #response = opener.open(x)
        response = GLOBAL_REQUEST_SESSION.get(x, timeout=GLOBAL_TIMEOUT)
        expanded = response.url
    except requests.Timeout as e:
        expanded = e.request.url
        return x, expanded, 1 # TIMEOUT
    except requests.RequestException as e:
        expanded = e.request
        if hasattr(expanded, "url"):
            expanded = expanded.url
        else:
            expanded = x
        return x, expanded, 3 # 404 or other error
    except Exception as e:
        return x, x, 2 # FAILED
    return x, expanded, 0 # SUCCESS EXPANSION

def expand_urls(url_input, url_output, url_resume=None,
        n_jobs=1, batches=10):
    resume_urls = set()
    with open(url_output, "wb+") as fp:
        if url_resume:
            with open(url_resume) as fpr:
                for line in fpr:
                    line = line.strip()
                    print >> fp, line
                    line = line.split('\t')[0]
                    resume_urls.add(line)
                print >> sys.stderr, "Resume has %s urls" % len(resume_urls)

    with open(url_input) as fp:
        all_urls = set([line.strip().split('\t')[0]
                for line in fp])
        print >> sys.stderr, "Input has %s urls" % len(all_urls)
        all_urls = list(all_urls - resume_urls)
    max_len = len(all_urls)
    batch_size = max_len / batches
    print >> sys.stderr, "Procesing %s urls in %s batches with %s batch size" % (
            max_len, batches, batch_size)
    
    with open(url_output, "ab+") as fp: ## Append to file as result was written before
        for start_idx in xrange(0,max_len, batch_size):
            end_idx = start_idx + batch_size
            expanded_urls = Parallel(n_jobs=n_jobs, verbose=1)(
                    delayed(get_url)(x)
                    for x in all_urls[start_idx:end_idx])
            for urls in expanded_urls:
                print >> fp, "%s\t%s\t%s" % urls
        print >> sys.stderr, "Processed %s urls" % len(expanded_urls)

if __name__ == "__main__":
    url_input='all_urls.txt'
    url_output='url_expanded.full.txt'
    n_jobs=1
    batches = 10
    
    import argparse
    parser = argparse.ArgumentParser(description='Expand URLs')
    parser.add_argument("--input", default=url_input, type=str,
            help="Input file with 1 URL per line.")
    parser.add_argument("--output", default=url_output, type=str,
            help="Output file")
    parser.add_argument("--resume", default=None,
            help="Resume file same as output file.")
    parser.add_argument("--jobs", default=n_jobs, type=int,
            help="Number of parallel jobs for joblib. [-1] for using all CPU cores.")
    parser.add_argument("--batches", default=batches, type=int,
            help="Batch size.")
    parser.add_argument("--timeout", default=GLOBAL_TIMEOUT, type=int,
            help="Timeout in seconds")

    args = parser.parse_args()
    url_input = args.input
    url_output = args.output
    url_resume = args.resume
    n_jobs = args.jobs
    batches = args.batches
    GLOBAL_TIMEOUT = args.timeout
    
    print >> sys.stderr, "Parsed arguments: %s" % args

    expand_urls(url_input, url_output, url_resume=url_resume,
            n_jobs=n_jobs, batches=batches)
