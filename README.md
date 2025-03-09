# Sai Amartya's Personal Website

A personal "brag website" to showcase projects, accomplishments, and blog posts. Built with Flask, MongoDB, and Bootstrap.

## Features

- **Projects Showcase**: Display your coding projects with descriptions, images, and links.
- **Accomplishments Section**: Highlight awards, certifications, education, and other achievements.
- **Blog**: Share your thoughts and insights with a built-in blog system.
- **Contact Form**: Allow visitors to send you messages directly from the website.
- **Admin Dashboard**: Manage all content through a secure admin interface.
- **Responsive Design**: Looks great on all devices from mobile to desktop.

## Tech Stack

- **Backend**: Flask (Python)
- **Database**: MongoDB
- **Frontend**: Bootstrap 5, HTML, CSS, JavaScript
- **Authentication**: Flask-Login
- **Forms**: Flask-WTF
- **Email**: SMTP via Python's built-in email library
- **Deployment**: Vercel

## Setup and Installation

### Prerequisites

- Python 3.8+
- MongoDB Atlas account (for database)
- Email account for sending notifications

### Local Development

1. Clone the repository:
   ```
   git clone <repository-url>
   cd personalsite
   ```

2. Create a virtual environment and install dependencies:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. Create a `.env` file in the root directory with the following variables:
   ```
   SECRET_KEY=your_secret_key_here
   MONGODB_URI=mongodb+srv://your_mongodb_connection_string
   ADMIN_PASSWORD=your_admin_password
   EMAIL_USER=your_email@example.com
   EMAIL_PASSWORD=your_email_password
   TINYMCE_API_KEY=your_api_key_here
   ```

4. Run the application:
   ```
   python run.py
   ```

5. Access the website at `http://localhost:5000`

## Deployment

See the [DEPLOYMENT.md](DEPLOYMENT.md) file for detailed instructions on deploying to Vercel with MongoDB Atlas.

## Project Structure

```
personalsite/
├── app/
│   ├── models/
│   │   ├── user.py
│   │   └── content.py
│   ├── routes/
│   │   ├── main.py
│   │   ├── auth.py
│   │   ├── admin.py
│   │   ├── projects.py
│   │   ├── accomplishments.py
│   │   ├── blog.py
│   │   └── contact.py
│   ├── static/
│   │   ├── css/
│   │   ├── js/
│   │   └── images/
│   ├── templates/
│   │   ├── admin/
│   │   ├── auth/
│   │   ├── blog/
│   │   ├── projects/
│   │   ├── accomplishments/
│   │   └── ...
│   ├── utils.py
│   ├── forms.py
│   └── __init__.py
├── venv/
├── .env
├── .gitignore
├── requirements.txt
├── run.py
├── DEPLOYMENT.md
└── README.md
```

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Contact

Sai Amartya - saiamartya19@gmail.com 