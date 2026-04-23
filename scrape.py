import urllib.request
from html.parser import HTMLParser

class ReasonParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.in_reason = False
        self.reasons = []
        self.current_data = []

    def handle_starttag(self, tag, attrs):
        if tag == 'div':
            for attr in attrs:
                if attr[0] == 'class' and attr[1] and 'h4 reason-title bold' in attr[1]:
                    self.in_reason = True
                    self.current_data = []

    def handle_endtag(self, tag):
        if tag == 'div' and self.in_reason:
            self.in_reason = False
            if self.current_data:
                self.reasons.append("".join(self.current_data).strip())

    def handle_data(self, data):
        if self.in_reason:
            self.current_data.append(data)

url = "https://fedena.com/101-reasons"
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'})
try:
    response = urllib.request.urlopen(req)
    html = response.read().decode('utf-8')
    parser = ReasonParser()
    parser.feed(html)
    for i, reason in enumerate(parser.reasons):
        print(f"{i+1}. {reason}")
except Exception as e:
    print(f"Error: {e}")
