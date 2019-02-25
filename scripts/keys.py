def _read_first_line(name):
	f = open(name, 'r')
	return f.read().strip().split()[0]

def access_key():
	filename = "keys/ACCESS_KEY"
	return _read_first_line(filename)

def secret_key():
	filename = "keys/SECRET_KEY"
	return _read_first_line(filename)