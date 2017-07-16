import os
from flask import Flask, request, redirect, url_for, render_template, flash
from werkzeug.utils import secure_filename
import main

UPLOAD_FOLDER = './uploads'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])

app = Flask(__name__)
app.secret_key = "super secret key"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        fileIn = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if fileIn.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if fileIn and allowed_file(fileIn.filename):
            filename = secure_filename(fileIn.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            fileIn.save(filepath)

            # Format the raw input into the required format
            spots = formatSpots(request.form)

            # Call the method to find if there's an open spot
            # Return the result to the view
            result = main.ProcessParking(filepath, spots)
            realResult = []

            for i, val in enumerate(result):
                if val > 0.008:
                    realResult.append("Spot " + str(i+1) + ": Occuppied")
                else:
                    realResult.append("Spot " + str(i+1) + ": Free")

            return render_template("result.html", result=realResult)
    return render_template("index.html")

def formatSpots(rawSpots):
    spots = {}
    for key in rawSpots:
        spots[key] = [tuple(map(int, x.split(','))) for x in rawSpots[key].split(';')]

    return spots

if __name__ == "__main__":
    app.run()
