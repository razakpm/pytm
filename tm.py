#!/usr/bin/env python3

from pytm.pytm import TM, Server, Database, Dataflow, Boundary, Actor


tm = TM("my test tm")
tm.description = "another test tm"

User_Web = Boundary("User/Web")
Web_DB = Boundary("Web/DB")

user = Actor("User")
user.inBoundary = "User/Web"

web = Server("Web Server")
web.OS = "CloudOS"
web.isHardened = True

db = Database("SQL Database (*)")
db.OS = "CentOS"
db.isHardened = False
db.inBoundary = "Web/DB"

user_to_web = Dataflow(user, web, "User enters comments (*)")
user_to_web.protocol = "HTTP"
user_to_web.dstPort = 80
user_to_web.data = 'Comments in HTML or Markdown'

web_to_user = Dataflow(web, user, "Comments saved (*)")
web_to_user.protocol = "HTTP"
web_to_user.data = 'Ack of saving or error message, in JSON'

web_to_db = Dataflow(web, db, "Insert query with comments")
web_to_db.protocol = "MySQL"
web_to_db.dstPort = 3306
web_to_db.data = 'MySQL insert statement, all literals'

db_to_web = Dataflow(db, web, "Comments contents")
db_to_web.protocol = "MySQL"
db_to_web.data = 'Results of insert op'

tm.process()
