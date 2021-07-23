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
    return render_template('wt_summary.html', rides=rides_list)


# Edit Times:
@waittimes.route('/edit')
@login_required
def wait_edit(rides_list=[]):
    rides_list = Ride.query.all() or rides_list
    return render_template('wt_edit.html', rides=rides_list)
