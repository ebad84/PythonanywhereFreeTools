from requests_html import HTMLSession


def login_and_extend(username="username", password="password"):
    session = HTMLSession()
    req = session.get("https://www.pythonanywhere.com/login/")
    csrfmiddlewaretoken = req.html.find('input[name="csrfmiddlewaretoken"]', first=True).attrs.get("value")
    form = {
        "csrfmiddlewaretoken":csrfmiddlewaretoken,
        "auth-username":username,
        "auth-password":password,
        "login_view-current_step":"auth"
    }
    session.headers.update({'Referer': 'https://www.pythonanywhere.com/login/'})
    req = session.post("https://www.pythonanywhere.com/login/", data=form)
    req = session.get(f"https://www.pythonanywhere.com/user/{username}/tasks_tab/")
    csrfmiddlewaretoken = req.html.find('input[name="csrfmiddlewaretoken"]', first=True).attrs.get("value")
    req = session.get(f"https://www.pythonanywhere.com/api/v0/user/{username}/schedule/")
    extend_url = "https://www.pythonanywhere.com"+req.json()[0]["extend_url"]
    session.headers.update({"X-CSRFToken":csrfmiddlewaretoken})
    req = session.post(extend_url)
    # print(req.text)
    print(req.status_code)
    return req.status_code