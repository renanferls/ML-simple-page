# Imports section
from flask import Flask, render_template, request, redirect, url_for, flash
from utils import corn_types, corn_names
from werkzeug.utils import secure_filename
import os
import datetime
# ------------------------------------------------------------------
# Local Imports
from functions import predictionWithCNN, imageSegmentation

# ------------------------------------------------------------------

# Application config
app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'
upload_folder = os.path.join('static', 'images')
app.config['UPLOAD'] = upload_folder
app.jinja_env.filters['zip'] = zip
app.jinja_env.filters['enumerate'] = enumerate
app.jinja_env.filters['round'] = round
# ------------------------------------------------------------------
# Local vars
classes = [
    "blanco",
    "chullpi",
    "cristalino",
    "morado",
    "morocho",
    "paro",
    "piscorunto",
    "san-geronimo"
]
# App routes

# ------------------------------------------------------------------
@app.route("/", methods=["GET", "POST"])
def index():
    return render_template("index.html")
# ------------------------------------------------------------------
@app.route("/information")
def information():
    my_variable = request.args.get('corn_type')
    context = {
        'corn_name': corn_names[str(my_variable)],
        'corn_description': corn_types[str(my_variable)]
    }
    return render_template(
            "corn_info.html",
            corn_name=context["corn_name"], 
            corn_description=context["corn_description"]
        )
# ------------------------------------------------------------------
@app.route("/load_image", methods=["GET", "POST"])
def load_image():
    if request.method == "POST":
        image = request.files["image"]
        if image:
            # save the image
            filename = secure_filename(image.filename)
            if len(filename.split("-")) > 1:
                ext = filename.split(".")[-1]
                local_time = datetime.datetime.now().strftime("%H_%M")
                filename = f"re_img_{local_time}.{ext}"
            image.save(os.path.join(app.config['UPLOAD'], filename))
            return redirect(url_for("result", img=filename))
        else:
            pass
    return render_template("load_image.html")
# ------------------------------------------------------------------
@app.route("/result/<img>")
def result(img):
    if img == "" or None:
        print("No filename specified")
    
    image_url = os.path.join("/", app.config['UPLOAD'], img)
    print("url for image: ", image_url)

    # Process the image

    segmented_image, edges_image, features_image = imageSegmentation(image_url)
    print(segmented_image, edges_image, features_image)

    array, position, time = predictionWithCNN(image_url)
    prediction = classes[position].capitalize()
    print("prediction for image: ", prediction)
    

    return render_template(
            "result.html", 
            image_url=image_url, 
            prediction=prediction, 
            segmented_image=f"/{segmented_image}", 
            edges_image=f"/{edges_image}", 
            features_image=f"/{features_image}"
        )
# ------------------------------------------------------------------
@app.route("/comparative", methods=["GET", "POST"])
def comparative():
    if request.method == "POST":
        image = request.files["image"]
        if image:
            # save the image
            filename = secure_filename(image.filename)
            if len(filename.split("-")) > 1:
                ext = filename.split(".")[-1]
                local_time = datetime.datetime.now().strftime("%H_%M")
                filename = f"re_img_{local_time}.{ext}"
            image.save(os.path.join(app.config['UPLOAD'], filename))
            return redirect(url_for("comparative_result", img=filename))
        else:
            pass
    return render_template("comparative.html")
# ------------------------------------------------------------------
@app.route("/comparative-result/<img>")
def comparative_result(img):
    if img == "" or None:
        print("No filename specified")
    
    image_url = os.path.join("/", app.config['UPLOAD'], img)

    array_1, position_1, time_1 = predictionWithCNN(image_url)
    prediction_1 = classes[position_1].capitalize()
    array_2, position_2, time_2 = predictionWithCNN(image_url)
    prediction_2 = classes[position_2].capitalize()
    precision_1 = array_1[0][position_1]*100
    precision_2 = array_2[0][position_2]*100
    return render_template(
            "comparative_result.html", 
            src_image=image_url,
            metodo_1="CNN",
            metodo_2="KNN",
            prediction_1=prediction_1, 
            prediction_2=prediction_2,
            precision_1=round(precision_1, 4),
            precision_2=round(precision_2, 4),
            array_1 = [round(num, 4)*100 for num in array_1[0]],
            array_2 = [round(num, 4)*100 for num in array_2[0]],
            time_1=time_1,
            time_2=time_2,
            classes=classes,
            zip=zip,
            enumerate=enumerate,
            round=round,
        )
# ------------------------------------------------------------------



# Application launch 
if __name__ == "__main__":
    app.run(debug=True)
# ------------------------------------------------------------------
