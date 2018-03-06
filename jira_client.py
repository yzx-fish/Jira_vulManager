import requests
# _*_ coding:utf-8 _*_


class JiraClient(object):
    API_URL = 'rest/api/2/'

    def __init__(self, host, user, password):
        self.host = host
        self.user = user
        self.password = password

    def search(self, software_name, project="SEC", status="undo"):
        if status == "undo":
            status = "(\"In Progress\", Backlog, \"Selected for Development\", \"won't fix\")"
        else:
            status = "(Done, \"wait for test\")"
        jql = "project = %s AND status in %s AND resolution = Unresolved AND text ~ \"%s\"" \
              " ORDER BY priority DESC, updated DESC" % (project, status, software_name)
        data = {
            "jql": jql,
            "startAt": 0,
            "maxResults": 600,
            "fields": ["summary", "assignee"]
        }
        return self._post(self.API_URL + 'search', data=data, params=None)

    def get_issue(self, issue_id, params=None):
        return self._get(self.API_URL + 'issue/{}'.format(issue_id), params=params)

    def create_issue(self, data, params=None):
        return self._post(self.API_URL + 'issue', data=data, params=params)

    def delete_issue(self, issue_id, params=None):
        return self._delete(self.API_URL + 'issue/{}'.format(issue_id), params=params)

    def _get(self, path, params=None):
        response = requests.get(self.host + path, params=params, auth=(self.user, self.password))
        return self._parse(response)

    def _post(self, path, params=None, data=None):
        response = requests.post(self.host + path, params=params, json=data, auth=(self.user, self.password))
        return self._parse(response)

    def _delete(self, path, params=None):
        response = requests.delete(self.host + path, params=params, auth=(self.user, self.password))
        return self._parse(response)

    def _parse(self, response):
        status_code = response.status_code
        if 'application/json' in response.headers['Content-Type']:
            r = response.json()
        else:
            r = response.text
        if status_code in (200, 201):
            return r
        if status_code == 204:
            return None
        message = None
        try:
            if 'errorMessages' in r:
                message = r['errorMessages']
        except Exception:
            message = 'No error message.'
        if status_code == 400:
            raise "[InvalidIDError]:" + message
        if status_code == 401:
            raise "[NotAuthenticatedError]:" + message
        if status_code == 403:
            raise "[PermissionError]:" + message
        if status_code == 404:
            raise "[NotFoundIDError]:" + message
        raise "[UnknownError]:" + message
