# -*- coding: utf-8 -*-
from flask import Flask, request
# TO generate UI for sending request via browser
from flasgger import Swagger
import numpy as np
from keras.preprocessing import image
from keras.models import model_from_json
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)

# Enable this app for swagger and it will auto generate UI
swagger = Swagger(app)


@app.route('/sign_img', methods=['POST'])
def predict_sign_file():
    # BELOW docstring lines are required to support swagger documentation
    """ Endpoint returning Sign prediction
    ---
    parameters:
        - name: input_file
          in: formData
          type: file
          required: true
    """

    print("In sign collection")
    img = request.files["input_file"]

    # Checks os to find path for tmp file
    if os.name == "posix":
        tmp_file = "/tmp/"
    elif os.name == "nt":
        tmp_file = "C:\\temp\\"
    else:
        tmp_file = input("What is your temp file absolute path: ")

    img.save(os.path.join(tmp_file, secure_filename(img.filename)))
    in_image = image.load_img(os.path.join(tmp_file, secure_filename(img.filename)), target_size=(50, 50))
    in_image = image.img_to_array(in_image)
    in_image = np.expand_dims(in_image, axis=0)

    print("Sign image collected")
    print(in_image)

    # Load model
    json_file = open('signimg_class_json/cnn.json', 'r')
    loaded_model_json = json_file.read()
    json_file.close()

    print("Model loaded Successfully")

    loaded_model = model_from_json(loaded_model_json)
    # load weights into new model
    loaded_model.load_weights("signimg_class_json/cnn.h5")

    # Make prediction using the input data
    prediction = loaded_model.predict(in_image)
    print(prediction)

    # Send the prediction as response - will need to convert number to string
    print("Returning prediction: ", prediction)
    for i, val in enumerate(prediction[0]):
        if val == 1.0:
            return "Sign was: "+ str(i)
    return "No prediction was available"


if __name__ == '__main__':
    app.run(debug=True)
