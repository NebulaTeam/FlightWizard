from flask import Flask, request, render_template, flash
from weather_grapper import WeatherGrapper as WG

SECRET_KEY = "Nebula Team"

app = Flask(__name__)

OWM_ICON_DESC = {'01': 'clear sky', '02': 'few clouds', '03': 'scattered clouds', '04': 'broken clouds', '09': 'shower rain', '10': 'rain', '11': 'thunderstorm', '13': 'snow', '50': 'mist' }

@app.route("/", methods=['GET', 'POST'])
def index():
	if request.method == 'POST':
		print(request.form['src'], request.form['dest'], request.form['dep_time'])

		if request.form['src'] == request.form['dest']:
			return render_template("index.html", error="Source and destinations can not be the same")

		grapper = WG(request.form['src'], request.form['dest'], request.form['dep_time'])
		srcW, destW = grapper.src_weather(), grapper.dest_weather()

		result = is_delayed(srcW) and is_delayed(destW)
		print(result, srcW, destW)

		return render_template("index.html", result=result, src_weather=srcW, dest_weather=destW, icons=OWM_ICON_DESC)
	else:
		return render_template("index.html")

def is_delayed(weather_tuple):
	will_be_delayed = True
	if weather_tuple[1] > 0.5:
		will_be_delayed = False
	# 1 m/s = 1.9438444924574 Knot
	if float(weather_tuple[0].get_wind()['speed']) < 58.315:
		will_be_delayed = False
	return will_be_delayed