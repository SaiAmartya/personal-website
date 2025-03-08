from flask import Blueprint, render_template, redirect, url_for, flash, current_app, request
from app.forms import ContactForm
from app.models.content import ContactMessage
from app.utils import send_email
from datetime import datetime
import os

contact = Blueprint('contact', __name__)

@contact.route('/contact', methods=['GET', 'POST'])
def contact_page():
    form = ContactForm()
    if form.validate_on_submit():
        # Create contact message
        message = ContactMessage()
        message.name = form.name.data
        message.email = form.email.data
        message.subject = form.subject.data
        message.message = form.message.data
        message.created_at = datetime.now()
        
        # Save to database
        current_app.db.contact_messages.insert_one(message.to_dict())
        
        # Send email notification
        admin_email = os.getenv('EMAIL_USER')
        email_body = f"""
        <h2>New Contact Message</h2>
        <p><strong>From:</strong> {message.name} ({message.email})</p>
        <p><strong>Subject:</strong> {message.subject}</p>
        <p><strong>Message:</strong></p>
        <p>{message.message}</p>
        """
        
        send_email(admin_email, f"New Contact Message: {message.subject}", email_body)
        
        flash('Your message has been sent! I will get back to you soon.', 'success')
        return redirect(url_for('contact.contact_page'))
    
    return render_template('contact.html', title='Contact', form=form) 