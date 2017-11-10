from openfalconclient.client import FalconClient
cli = FalconClient(endpoint="http://127.0.0.1:8080", user='admin', password='admin123')
# ex api/v1/user/users  get
r = cli.user.users.list()

# /api/v1/user/name/xxxx  get
r = cli.user.name['admin'].get()

# /api/v1/user/u/xxxx get
r = cli.user.u['1'].get()

# /api/v1/user/update  put
params = {
  "name": "test1",
  "cnname": "est",
  "email": "root123@cepave.com",
  "im": "44955834958",
  "phone": "99999999999",
  "qq": "904394234239"
}
cli.user.update.update(params=params)

# /api/v1/admin/delete_user  delete
params = {"user_id": 31}
cli.admin.delete_user.delete(params=params)

# /api/v1/template/7    delete
cli.template['7'].delete()