from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required
from waittimes.models import Ride
from waittimes.rides.forms import UpdateRideForm


rides = Blueprint('rides', __name__)


# Rides Dashboard:
@rides.route('/dashboard')
@login_required
def ride_dashboard(rides_list=[]):
    rides_list = Ride.query.all() or rides_list
    return render_template('rides/ride_dashboard.html', rides=rides_list)


# Change Ride Info:
@rides.route('/edit/<int:ride_id>', methods=['GET', 'POST'])
@login_required
def edit_ride_info(ride_id):
    ride = Ride.query.get_or_404(ride_id)
    form = UpdateRideForm()
    # Form is validated before submit:
    if form.validate_on_submit():
        changes_made = False

        # If ride name was changed, update ride:
        if form.name.data != ride.name:
            name = ride.name
            ride.name = form.name.data
            flash(f"Ride name was changed from \"{name}\" to \"{ride.name}\"",
                  'success')
            changes_made = True
            
        # If ride status was changed, update ride:
        if form.status.data != ride.status:
            status = ride.status
            ride.status = form.status.data
            flash(f"Ride status was changed from {status} to {ride.status}",
                  'success')
            changes_made = True
            
        # Ride image URL is updated if it was changed:
        if form.image_url.data != ride.image:
            ride.image = form.image_url.data
            flash(f"Ride image updated.", 'success')
            changes_made = True
            
        # Ride notes get updated if they were changed:
        if form.notes.data != ride.optional_notes:
            ride.optional_notes = form.notes.data
            flash(f"Ride notes updated.", 'success')
            changes_made = True
        
        # If any changes were made, save the ride:
        if changes_made:
            ride.save_changes()
        else:
            flash("No Changes Were Made", 'info')

        return redirect(url_for('rides.edit_ride_info', ride_id=ride_id))

    # Populate form with rides current info:
    form.name.data = ride.name
    form.status.data = ride.status
    form.image_url.data = ride.image
    form.notes.data = ride.optional_notes
    return render_template('rides/ride_edit.html', ride=ride, form=form)


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