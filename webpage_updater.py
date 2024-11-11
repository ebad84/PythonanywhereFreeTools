from requests_html import HTMLSession

def login_and_webapp_extend(username="username", password="password"):
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
    req = session.get(f"https://www.pythonanywhere.com/user/{username}/webapps/")
    csrfmiddlewaretoken = req.html.find('input[name="csrfmiddlewaretoken"]', first=True).attrs.get("value")
    webapp_extend_url = f"https://www.pythonanywhere.com/user/{username}/webapps/{username}.pythonanywhere.com/extend"
    session.headers.update({"X-CSRFToken":csrfmiddlewaretoken})
    req = session.post(webapp_extend_url, data={"csrfmiddlewaretoken":csrfmiddlewaretoken})
    # print(req.text)
    print(req.status_code)
    return req.status_code

login_and_webapp_extend()