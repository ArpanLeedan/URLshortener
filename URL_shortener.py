from flask import Flask, render_template, request, redirect, url_for
import requests

app = Flask(__name__)

BITLY_USERNAME = "enter user id"
BITLY_PASSWORD = 'enter bitly password'

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        url = request.form['url']

        # get the access token
        auth_res = requests.post("https://api-ssl.bitly.com/oauth/access_token", auth=(BITLY_USERNAME, BITLY_PASSWORD))
        if auth_res.status_code == 200:
            access_token = auth_res.content.decode()
        else:
            return render_template('index1.html', error="Cannot get access token, check your credentials.")

        headers = {"Authorization": f"Bearer {access_token}"}

        # get the group UID associated with our account
        groups_res = requests.get("https://api-ssl.bitly.com/v4/groups", headers=headers)
        if groups_res.status_code == 200:
            groups_data = groups_res.json()['groups'][0]
            guid = groups_data['guid']
        else:
            return render_template('index1.html', error="Cannot get GUID, please try again later.")

        # make the POST request to get shortened URL for `url`
        shorten_res = requests.post("https://api-ssl.bitly.com/v4/shorten", json={"group_guid": guid, "long_url": url}, headers=headers)
        if shorten_res.status_code == 200:
            link = shorten_res.json().get("link")
            return render_template('index1.html', short_url=link)
        else:
            return render_template('index1.html', error="Failed to shorten the URL, please try again.")

    return render_template('index1.html')

if __name__ == '__main__':
    app.run(debug=True)
