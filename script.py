from flask import Flask, render_template, request, send_file
import pandas
from geopy.geocoders import Nominatim
app=Flask(__name__)

@app.route('/')
def home():
    return render_template("home.html")

@app.route('/success', methods=['POST'])
def success():
    if request.method == 'POST':
        file=request.files["file"]
        file.save("s"+file.filename)
        df=pandas.read_csv("s"+file.filename)
        n=Nominatim()
        for a in df["Address"]:
            r=n.geocode(a)
            df["lat"]=r.latitude
            df["lon"]=r.longitude
        df.to_csv("done.csv")
        return render_template("home.html", btn="download.html", text=df.to_html())

@app.route('/download')
def download():
    return send_file("done.csv",attachment_filename="updatedfile.csv",as_attachment=True)

if __name__ == "__main__":
    app.run(debug=True)