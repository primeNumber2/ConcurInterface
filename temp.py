def test(sql):
    return "Hello " + sql

li = "morning"
print test("Frank %s" % li)