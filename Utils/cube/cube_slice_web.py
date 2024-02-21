import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from flask import Flask, render_template, request
import io
import base64
import urllib
from cube_slice import plot_cube

def run_web():
    matplotlib.use('Agg')

    app = Flask(__name__)

    @app.route('/', methods=['GET', 'POST'])
    def home():
        point1 = [80, 0, 100]
        point2 = [100, 20, 100]
        point3 = [100, 0, 80]
        
        if request.method == 'POST':
            # Get points from form
            point1 = np.array([int(request.form['point1_x']), int(request.form['point1_y']), int(request.form['point1_z'])])
            point2 = np.array([int(request.form['point2_x']), int(request.form['point2_y']), int(request.form['point2_z'])])
            point3 = np.array([int(request.form['point3_x']), int(request.form['point3_y']), int(request.form['point3_z'])])

            # Plot the cube
            plot_cube(point1, point2, point3)

            # Show the plot
            # plt.show()

            # Convert plot to PNG image
            png_image = io.BytesIO()
            plt.savefig(png_image, format='png')
            png_image.seek(0)
            png_image = 'data:image/png;base64,' + urllib.parse.quote(base64.b64encode(png_image.read()))

            return render_template('home.html', png_image=png_image, point1=point1, point2=point2, point3=point3)

        return render_template('home.html', point1=point1, point2=point2, point3=point3)

    if __name__ == '__main__':
        app.run(debug=True, host='0.0.0.0', port=5002)

run_web()