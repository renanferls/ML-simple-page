# Imports section
from flask import Flask, render_template, request, redirect, url_for, flash
from utils import corn_types, corn_names
# ------------------------------------------------------------------

# Application config
app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'
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
@app.route("/process_image")
def process_image():
    return render_template("process_image.html")
# ------------------------------------------------------------------
@app.route("/history")
def history():
    return render_template("result.html")
# ------------------------------------------------------------------
# @app.route("/process/<filename>")
# def process_image(filename):
#     if filename == "" or None:
#         flash("Please Select Image")
#     """ 
#     Validate incoming request parameters
#     """


#     image_url = "/static/images/" + filename

#     """ 
#     Logic for start processing with models

#     ...
    
#     """

#     return render_template("process.html", image_url=image_url)

# Application launch 
if __name__ == "__main__":
    app.run(debug=True)
# ------------------------------------------------------------------
