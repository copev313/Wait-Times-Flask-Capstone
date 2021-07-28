import waittimes
from flask import Blueprint, render_template
from flask_login import login_required
from waittimes.models import Ride


waittimes = Blueprint('waittimes', __name__)


# Summary Report:
@waittimes.route('/summary')
@login_required
def wait_summary():
    rides_list = Ride.query.all()
    return render_template('wait_times/wt_summary.html', rides=rides_list)


# Edit Times:
@waittimes.route('/edit/<int:ride_id>')
@login_required
def wait_edit(ride_id):
    ride = Ride.query.get_or_404(ride_id)
    return render_template('wait_times/wt_edit.html', ride=ride)
