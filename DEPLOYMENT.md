# Deployment Guide

This guide will walk you through deploying your personal website using MongoDB Atlas for the database and Vercel for hosting. We'll use GitHub for version control and continuous deployment.

## Step 1: Set Up MongoDB Atlas

1. **Create a MongoDB Atlas Account**:
   - Go to [MongoDB Atlas](https://www.mongodb.com/cloud/atlas) and sign up for a free account.
   - Create a new organization if prompted.

2. **Create a New Project**:
   - Name your project (e.g., "Personal Website").
   - Click "Create Project".

3. **Create a Database**:
   - Click "Build a Database".
   - Choose the "Free" shared cluster option.
   - Select your preferred cloud provider and region (choose one close to your target audience).
   - Click "Create Cluster".

4. **Set Up Database Access**:
   - In the left sidebar, click "Database Access" under "Security".
   - Click "Add New Database User".
   - Create a username and a strong password. Save these credentials securely.
   - Set privileges to "Read and Write to Any Database".
   - Click "Add User".

5. **Configure Network Access**:
   - In the left sidebar, click "Network Access" under "Security".
   - Click "Add IP Address".
   - For development, you can add your current IP address.
   - For production, select "Allow Access from Anywhere" (0.0.0.0/0).
   - Click "Confirm".

6. **Get Your Connection String**:
   - Once your cluster is created, click "Connect".
   - Select "Connect your application".
   - Copy the connection string.
   - Replace `<password>` with your database user's password.
   - Replace `myFirstDatabase` with a name for your database (e.g., "personal_site").

## Step 2: Set Up GitHub Repository

1. **Create a New Repository**:
   - Go to [GitHub](https://github.com) and sign in.
   - Click the "+" icon in the top right and select "New repository".
   - Name your repository (e.g., "personal-website").
   - Choose "Private" or "Public" visibility.
   - Click "Create repository".

2. **Push Your Code to GitHub**:
   - Initialize Git in your project folder (if not already done):
     ```
     git init
     ```
   - Add your files:
     ```
     git add .
     ```
   - Commit your changes:
     ```
     git commit -m "Initial commit"
     ```
   - Add the remote repository:
     ```
     git remote add origin https://github.com/yourusername/your-repo-name.git
     ```
   - Push your code:
     ```
     git push -u origin main
     ```

## Step 3: Set Up Vercel

1. **Create a Vercel Account**:
   - Go to [Vercel](https://vercel.com) and sign up using your GitHub account.

2. **Import Your GitHub Repository**:
   - Click "Import Project" on your Vercel dashboard.
   - Select "Import Git Repository".
   - Choose your personal website repository from the list.

3. **Configure Project Settings**:
   - Project Name: Choose a name for your project (e.g., "sai-amartya-personal-site").
   - Framework Preset: Select "Other".
   - Root Directory: Leave as default (/).
   - Build Command: `pip install -r requirements.txt && python -m gunicorn run:app`
   - Output Directory: Leave blank.

4. **Set Environment Variables**:
   - Click "Environment Variables" to expand the section.
   - Add the following variables:
     - `SECRET_KEY`: A random string for Flask security
     - `MONGODB_URI`: Your MongoDB Atlas connection string
     - `ADMIN_PASSWORD`: Your admin password for the website
     - `EMAIL_USER`: Your email address (saiamartya19@gmail.com)
     - `EMAIL_PASSWORD`: Your email password or app password

5. **Deploy**:
   - Click "Deploy".
   - Wait for the deployment to complete.

6. **Configure Custom Domain (Optional)**:
   - In your project settings, go to "Domains".
   - Add your custom domain and follow the instructions to set up DNS records.

## Step 4: Set Up Continuous Deployment

Vercel automatically sets up continuous deployment from your GitHub repository. Whenever you push changes to your main branch, Vercel will automatically rebuild and deploy your site.

1. **Make Changes to Your Site**:
   - Edit your code locally.
   - Commit and push to GitHub:
     ```
     git add .
     git commit -m "Update website"
     git push
     ```

2. **Monitor Deployments**:
   - Go to your Vercel dashboard to monitor the deployment status.
   - Click on your project to see deployment details and logs.

## Step 5: Test Your Website

1. **Check All Features**:
   - Visit your deployed website.
   - Test the admin login functionality.
   - Add a test project, accomplishment, and blog post.
   - Test the contact form.

2. **Mobile Responsiveness**:
   - Test your website on different devices and screen sizes.
   - Use browser developer tools to simulate different devices.

## Troubleshooting

### Database Connection Issues:
- Verify your MongoDB Atlas connection string is correct.
- Check that your IP address is allowed in the Network Access settings.
- Ensure your database user has the correct permissions.

### Deployment Failures:
- Check the Vercel deployment logs for errors.
- Verify that all required environment variables are set correctly.
- Make sure your code works locally before pushing to GitHub.

### Email Sending Issues:
- If using Gmail, you may need to create an "App Password" instead of using your regular password.
- Enable "Less secure app access" in your Google account settings.
- Consider using a transactional email service like SendGrid for production.

## Maintenance

### Regular Updates:
- Keep your dependencies updated for security and performance.
- Regularly backup your MongoDB database.

### Monitoring:
- Set up monitoring for your website using Vercel Analytics or Google Analytics.
- Regularly check your MongoDB Atlas dashboard for database performance.

## Conclusion

Your personal website is now deployed and accessible to the world! You can continue to make updates and improvements by pushing changes to your GitHub repository, and Vercel will automatically deploy them. 