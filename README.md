from openfalconclient.client import FalconClient
cli = FalconClient(endpoint="http://200.200.114.161:8080", user='admin', password='Admin12345')
# ex api/v1/user/users  post
r = cli.user.users.list()

# /api/v1/user/name/xxxx  get
r = cli.user.name['admin'].get()

# /api/v1/user/u/xxxx get
r = cli.user.u['1'].get()