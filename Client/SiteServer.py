from flask import Flask, render_template,request, url_for, redirect
import dal_SiteData
import dal_SiteUsers

app = Flask(__name__) # open object of flask

# Handling actions done inside the Login page - SQL Injection Vulnerability
@app.route("/",methods = ['GET','POST'] )
def main():
    if request.method =="POST":
        username = request.form["username"]
        password = request.form["password"]
        connection = dal_SiteUsers.connect_db()
        dal_SiteUsers.Add_users_to_DB()
        password = dal_SiteUsers.hash_to_pass(password)
        flag = dal_SiteUsers.in_DB(connection, username, password)
        if flag:
            return redirect(url_for('Home'))
        else:
            return render_template("Login.html")

    else:
        return render_template("Login.html")


# Handling actions done inside the Comment Section page - XSS Vulnerability
@app.route('/XSS', methods=['GET', 'POST'])
def XSS():
    connection = dal_SiteData.connect_db()
    dal_SiteData.clean_db(connection)
    if request.method =="POST":
        data = request.form["comment"]
        dal_SiteData.add_comment(connection, data)

    search_query = request.args.get('q')
    comments = dal_SiteData.get_comments(connection, search_query)
    return render_template("XSS.html",comments=comments,search_query=search_query)

# Routing to the Home page
@app.route("/Home")
def Home():
    return render_template("Home.html")




