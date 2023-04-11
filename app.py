from flask import Flask, request, render_template
from json import loads

app = Flask(__name__)

# Define the categories we want to include
CATEGORIES = ['general', 'image', 'video', 'news', 'book']

# Define the 'about' information
ABOUT = {
    "website": 'https://github.com/searx/searx',
    "wikidata_id": 'Q17639196',
    "official_api_documentation": 'https://searx.github.io/searx/dev/search_api.html',
    "use_official_api": True,
    "require_api_key": False,
    "results": 'JSON',
}

# Define the categories to search through
categories = [c for c in searx_categories.keys() if c.split(':')[0] in CATEGORIES]

# Define the instance URLs and index
instance_urls = ['https://paulgo.io/', 'https://www.gruble.de/', 'https://searx.tiekoetter.com/', 'https://baresearch.org/'; 'https://search.ononoki.org/']
instance_index = 0

# Define the search request function
def request_search(query, params):
    global instance_index
    params['url'] = instance_urls[instance_index % len(instance_urls)]
    params['method'] = 'POST'

    instance_index += 1

    params['data'] = {
        'q': query,
        'pageno': params['pageno'],
        'language': params['language'],
        'time_range': params['time_range'],
        'category': params['category'],
        'format': 'json'
    }

    return params

# Define the response handling function
def handle_response(resp):
    response_json = loads(resp.text)
    results = response_json['results']

    for i in ('answers', 'infoboxes'):
        results.extend(response_json[i])

    results.extend({'suggestion': s} for s in response_json['suggestions'])

    results.append({'number_of_results': response_json['number_of_results']})

    return results

# Define the routes
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search', methods=['GET', 'POST'])
def search():
    if request.method == 'POST':
        query = request.form['query']
        category = request.form['category']
        params = {
            'pageno': 1,
            'language': 'en-US',
            'time_range': '',
            'category': category,
            'format': 'json'
        }
        params = request_search(query, params)
        results = handle_response(params)

        if category == 'general':
            return render_template('general.html', results=results)
        elif category == 'image':
            return render_template('image.html', results=results)
        elif category == 'video':
            return render_template('video.html', results=results)
        elif category == 'news':
            return render_template('news.html', results=results)
        elif category == 'book':
            return render_template('book.html', results=results)

    return render_template('search.html')

if __name__ == '__main__':
    app.run(debug=True)