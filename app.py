from flask import Flask, render_template, request
from flask_pymongo import PyMongo
from bson.objectid import ObjectId

app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb://localhost:27017/mongo030"
mongo = PyMongo(app)

@app.route("/")
def homepage():
    return "to do homepage"

@app.route("/eisenhower", methods=["GET", "POST"])
def eisenhower():
    if request.method=="POST":
        delete_id = request.form.get("delete_task_id")
        task_id = request.form.get('task_id')
        title = request.form.get("task_title")
        desc = request.form.get("task_desc")
        important = True if request.form.get("important") else False
        urgent = True if request.form.get("urgent") else False
        if delete_id:
            mongo.db.tasks.delete_one({"_id": ObjectId(delete_id)})
        elif task_id:
            mongo.db.tasks.update_one(
                {"_id": ObjectId(task_id)},
                {"$set": {"title":title,
                "desc":desc,
                "important":important,
                "urgent":urgent}}
            )
        else:        
            mongo.db.tasks.insert_one({
                "title":title,
                "desc":desc,
                "important":important,
                "urgent":urgent
            })
    edit_id = request.args.get("edit")
    edit_task = None
    if edit_id:
        edit_task = mongo.db.tasks.find_one({"_id": ObjectId(edit_id)})

    task11 = mongo.db.tasks.find({"$and": [{"urgent": True}, {"important":True}]})
    task10 = mongo.db.tasks.find({"$and": [{"urgent": True}, {"important":False}]}) 
    task01 = mongo.db.tasks.find({"$and": [{"urgent": False}, {"important":True}]}) 
    task00 = mongo.db.tasks.find({"$and": [{"urgent": False}, {"important":False}]}) 
    tasks = {
        "task11":task11,
        "task10":task10,
        "task01":task01,
        "task00":task00,
    }
    return render_template("eisenhower.html", tasks=tasks, edit_task=edit_task)
if __name__=="__main__":
    app.run(debug=True)