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

# ------------------------------------------------------------------

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

    prediction = predictionWithCNN(image_url).capitalize()
    print("prediction for image: ", prediction)
    

    return render_template("result.html", image_url=image_url, prediction=prediction, segmented_image=f"/{segmented_image}", edges_image=f"/{edges_image}", features_image=f"/{features_image}")
# ------------------------------------------------------------------
@app.route("/history")
def history():
    return render_template("result.html")
# ------------------------------------------------------------------



# Application launch 
if __name__ == "__main__":
    app.run(debug=True)
# ------------------------------------------------------------------
