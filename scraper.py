from requests import get
from requests.exceptions import RequestException
from contextlib import closing
from bs4 import BeautifulSoup

def simple_get(url):
    """
    Attempts to get the content at `url` by making an HTTP GET request.
    If the content-type of response is some kind of HTML/XML, return the
    text content, otherwise return None.
    """
    try:
        with closing(get(url, stream=True)) as resp:
            if is_good_response(resp):
                return resp.content
            else:
                return None

    except RequestException as e:
        log_error('Error during requests to {0} : {1}'.format(url, str(e)))
        return None


def is_good_response(resp):
    """
    Returns True if the response seems to be HTML, False otherwise.
    """
    content_type = resp.headers['Content-Type'].lower()
    return (resp.status_code == 200
            and content_type is not None
            and content_type.find('html') > -1)


def log_error(e):
    """
    It is always a good idea to log errors.
    This function just prints them, but you can
    make it do anything.
    """
    print(e)


def get_exercises(url, file_name, name, netid):
    """
    Downloads the page where the list of exercises is found
    and creates a new .ml file with those exercises.
    """
    response = simple_get(url)
    f = open(file_name + ".ml", "w")
    f.write('(** @author ' + name + ' (' + netid + ')*)\n\n')
    if response is not None:
        html = BeautifulSoup(response, 'html.parser')
        names = set()
        for h5 in html.select('h5'):
            for name in h5.text.split('\n'):
                if len(name) > 0:
                    name = name.replace('✭', '*')
                    f.write('(** ' + name.strip() + '*)' + '\n\n\n')

    # Raise an exception if we failed to get any data from the url
    raise Exception('Error retrieving contents at {}'.format(url))

if __name__ == "__main__":
    get_exercises("http://www.cs.cornell.edu/courses/cs3110/2019sp/textbook/interp/exercises.html",
        "chapter9", "YOUR NAME", "YOUR NETID")
