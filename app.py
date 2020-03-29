from flask import Flask, render_template, request,redirect,flash,url_for,session
from flask_socketio import SocketIO, send, emit,join_room

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secretkey'
app.config['DEBUG'] = True
socketio = SocketIO(app)



@app.route('/')
def home():
    if session.get('uname') and session.get('room') :
        return render_template("room.html" ,u=session.get('uname'),r=session.get('room') )

    return render_template('home.html')


@app.route("/room",methods=["POST","GET"])
def room():
    if(request.method == "GET"):
        uname= session.get('uname')
        room=session.get('room')
    else:
        uname= request.form.get("uname")
        room=request.form.get("room")
        session["uname"]=uname
        session["room"]=room
    message = uname
    if uname == "" or uname == None:
        flash("enter a valid user name")
        return redirect(url_for("home"))
    else:
        return render_template("room.html" ,u=uname,r=room )

@socketio.on("join")
def join(data):
    app.logger.info("{} has joined the room {}".format(data['username'], data['room']))
    join_room(data["room"])
    socketio.emit("join_anouncement",data)



@socketio.on("send_text")
def send(data):
    app.logger.info("{} has sent {}".format(data['username'], data['text']))
    socketio.emit("recieve_msg",data,room= data['room'])

@app.route('/logout')
def logout():
    session["uname"]=None
    session["room"]=None
    return redirect(url_for("home"))


if __name__ == "__main__":
    socketio.run(app)
