from flask import Flask, render_template, request
import requests

app = Flask(__name__)

API_KEY = '** Pexel API KEY **'  # Replace this with your actual Pexels API key
IMAGE_API_URL = 'https://api.pexels.com/v1/search'
VIDEO_API_URL = 'https://api.pexels.com/videos/search'

@app.route('/', methods=['GET'])
def index():
    query = request.args.get('query', 'nature')
    content_type = request.args.get('type', 'image')
    page = int(request.args.get('page', 1))
    per_page = 4
    params = {'query': query, 'per_page': per_page, 'page': page}
    headers = {'Authorization': API_KEY}


    if content_type == 'video':
        response = requests.get(VIDEO_API_URL, headers=headers, params=params)
        content = response.json().get('videos', [])
    else:
        response = requests.get(IMAGE_API_URL, headers=headers, params=params)
        content = response.json().get('photos', [])

    total_results = response.json().get('total_results', 0)
    total_pages = (total_results + per_page - 1) // per_page

    return render_template('index.html', content=content, content_type=content_type,
                           page=page, total_pages=total_pages, query=query)

if __name__ == '__main__':
    app.run(debug=True)
