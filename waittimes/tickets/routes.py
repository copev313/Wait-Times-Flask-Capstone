from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_required


tickets = Blueprint('tickets', __name__)


# TICKETS --> Create Ticket:
@tickets.route('/create')
@login_required
def create_ticket():
    return render_template('tickets/ticket_create.html')


# TICKETS --> Edit Ticket:
@tickets.route('/edit')
@login_required
def edit_ticket():
    return render_template('tickets/ticket_edit.html')


# TICKETS --> Ticket Records:
@tickets.route('/records')
@login_required
def ticket_records():
    return render_template('tickets/ticket_records.html')


