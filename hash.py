import hashlib
m = hashlib.sha256()
m.update(b"Ta Dang Trung Kien")
x= m.hexdigest()
print(x)