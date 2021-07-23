from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_required
from waittimes.models import Ride


rides = Blueprint('rides', __name__)


# Rides Dashboard:
@rides.route('/dashboard')
@login_required
def ride_dashboard(rides_list=[]):
    rides_list = Ride.query.all() or rides_list
    return render_template('rides/ride_dashboard.html', rides=rides_list)


# Change Ride Info:
@rides.route('/edit/<int:ride_id>')
@login_required
def edit_ride_info(ride_id):
    ride = Ride.query.get_or_404(ride_id)
    return render_template('rides/ride_edit.html', ride=ride)


# Create Ride:
@rides.route('/create', methods=['GET', 'POST'])
@login_required
def create_ride():
    # [CASE] POST request:
    if (request.method == 'POST'):
        ride_name = request.form['name']
        ride = None

        if request.form['waittime']:
            ride_wt = request.form['waittime']
            ride = Ride(ride_name, ride_wt)
        else:
            ride = Ride(ride_name)

        if request.form['status']:
            ride_status = request.form['status']
            ride.set_ride_status(ride_status)
        
        if request.form['imagelink']:
            ride_img = request.form['imagelink']
            ride.set_ride_image(ride_img)

        if request.form['notes']:
            ride_notes = request.form['notes']
            ride.write_optional_notes(ride_notes)

        ride.create_ride()
        return redirect(url_for('create_ride'))

    return render_template('rides/ride_create.html')