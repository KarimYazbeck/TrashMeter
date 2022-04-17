from flask import Flask, redirect, url_for, render_template, request
import json
import os

app = Flask(__name__)

#########################################

#reasons_for = []
#reasons_against = []

def get_json_data_for():
    file = open('data2.json')
    data = json.load(file)

    print("//////////////////////////////")

    reasons_for2 = []
    #reasons_against = []
    reason = []

    for i in data:
        reason.append(i['reason'])
        reason.append(i['score'])
        if(i['type']=="for"):
            reasons_for2.append(reason)
        #else:
            #reasons_against.append(reason)
        reason = []

    '''
    print("Reasons For : ")
    for i in reasons_for:
        print(i)

    print("Reasons Against : ")
    for i in reasons_against:
        print(i)

    '''

    file.close()

    return reasons_for2


def get_json_data_aga():
    file = open('data2.json')
    data = json.load(file)

    print("//////////////////////////////")

    #reasons_for = []
    reasons_against = []
    reason = []

    for i in data:
        reason.append(i['reason'])
        reason.append(i['score'])
        if(i['type']=="against"):
            reasons_against.append(reason)
        #else:
            #reasons_against.append(reason)
        reason = []

    file.close()

    return reasons_against

reasons_for2 = get_json_data_for()
reasons_against2 = get_json_data_aga()

def update_json(reasons_for_HTML, scores_for_HTML, reasons_aga_HTML, scores_aga_HTML):

    data2 = []

    for i in range(len(reasons_for_HTML)):
        if (reasons_for_HTML[i] != '' and scores_for_HTML != ''):
            data2.append({'reason': reasons_for_HTML[i], 'score': scores_for_HTML[i], 'type':'for'})
        

    
    for i in range(len(reasons_aga_HTML)):
        if (reasons_aga_HTML[i] != '' and scores_aga_HTML != ''):
            data2.append({'reason': reasons_aga_HTML[i], 'score': scores_aga_HTML[i], 'type':'against'})
        

    # this is extremely important and will be a headache to automate (i'm excited)
    #data = [{'reason':'coffee', 'score':5, 'type':'for'}, {'reason':'health', 'score':3, 'type':'against'}]
    

    os.remove('data2.json')
    with open('data2.json', 'w') as file:
        #data = json.load(file)

        

        file.truncate()

        file.seek(0)
        
        

        json.dump(data2, file, indent=4)
        

        file.close()
        





# i want to pass the 2 lists as parameters
# i should modify html with jinja
# imma make a for loop which creates some inputs in the html file at each load
#              - these inputs will be filled from the lists
#              - ill make more empty inputs for the user to fill
# everytime the user submits the form i want to :
#              - rewrite the json file
#              - repopulate the form with the data from the json file

print("//////////////////////////////////")





#file.close()

#################################

def update_meter_value(scores_for, scores_aga):
    sum_for = 0
    sum_aga = 0

    for i in scores_for:
        if i != '':
            sum_for += int(i)

    for i in scores_aga:
        if i != '':
            sum_aga += int(i)

    sum_total = sum_for + sum_aga
    #print(sum_for)
    return int((sum_for / sum_total) * 100)



@app.route("/", methods=['POST', 'GET'])
def home():
    avg2 = 0
    if request.method == 'POST':
        reasons_for_HTML = request.form.getlist('reasons_for_HTML')
        scores_for_HTML = request.form.getlist('scores_for_HTML')
        reasons_aga_HTML = request.form.getlist('reasons_aga_HTML')
        scores_aga_HTML = request.form.getlist('scores_aga_HTML')
        print(reasons_for_HTML, scores_for_HTML, reasons_aga_HTML, scores_aga_HTML)
        update_json(reasons_for_HTML, scores_for_HTML, reasons_aga_HTML, scores_aga_HTML)
        reasons_for = get_json_data_for()
        reasons_against = get_json_data_aga()
        display_vals(reasons_for_HTML, scores_for_HTML, reasons_aga_HTML, scores_aga_HTML)
        avg2 = update_meter_value(scores_for_HTML, scores_aga_HTML)
        #return redirect(url_for('home'))
    #else:
    return render_template("index.html", reasons_for = reasons_for2, reasons_against = reasons_against2, avg = avg2)

def display_vals(reasons_for_HTML, scores_for_HTML, reasons_aga_HTML, scores_aga_HTML):
    print("((((((((((((((((((((((((((")
    print(reasons_for_HTML)
    print(scores_for_HTML)
    print(reasons_aga_HTML)
    print(scores_aga_HTML)
    
    #for i in reasons_for:
        #print(i)
    print(")))))))))))))))))))))))))")





@app.route('/login', methods=['POST','GET'])
def login():
    if request.method == 'POST':
        fname = request.form['firstName']
        lname = request.form['lastName']
        texta = request.form['texta']
        write_to_file(texta)
        return render_template("login.html")
        #return redirect(url_for("user", usr=fname, usrLast=lname))
    else:
        return render_template("login.html")

@app.route("/<usr>")
def user(usr):
    return f"<h1>{usr}</h1>"


def write_to_file(texta):
    f = open("data.txt", 'w')
    f.write(texta)
    f.close()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
    #app.run(host="0.0.0.0", port=5000)
    #app.run(debug=True)


