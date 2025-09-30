# College Fee Payment System

A comprehensive Django web application for managing college fee payments with MongoDB integration and Razorpay payment gateway.

## Features

### Student Features
- **Registration & Authentication**: Secure student registration with profile picture upload
- **Dashboard**: Modern dark-themed interface showing profile and fee information
- **Fee Payment**: Integration with Razorpay for secure online payments
- **Payment History**: View all past transactions with detailed information
- **Receipt Generation**: Download PDF receipts for completed payments
- **Profile Management**: View and manage student profile information

### Admin Features
- **Admin Dashboard**: Overview of students, payments, and revenue statistics
- **Student Management**: View all registered students with search and filter options
- **Fee Management**: Update fee amounts for individual students based on admission type
- **Payment Monitoring**: View payment histories and transaction details
- **Reporting**: Generate reports on fee collections and student payments

## Technical Stack

- **Backend**: Django 4.2.7
- **Database**: MongoDB with djongo adapter
- **Payment Gateway**: Razorpay
- **Frontend**: Bootstrap 5 with dark theme
- **PDF Generation**: ReportLab
- **Authentication**: Django sessions with custom user models

## Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd college_fee_system
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Environment Configuration**
   ```bash
   cp .env.example .env
   ```
   
   Update the `.env` file with your configuration:
   ```
   SECRET_KEY=your-secret-key-here
   DEBUG=True
   MONGO_URI=mongodb://localhost:27017
   MONGO_DB_NAME=college_fee_system
   RAZORPAY_KEY_ID=your-razorpay-key-id
   RAZORPAY_KEY_SECRET=your-razorpay-secret
   ```

5. **Database Setup**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

6. **Create Admin User**
   ```bash
   python manage.py shell
   ```
   
   In the Django shell:
   ```python
   from admins.models import Admin
   admin = Admin(
       username='admin',
       email='admin@college.edu',
       full_name='System Administrator',
       is_super_admin=True
   )
   admin.set_password('admin123')
   admin.save()
   ```

7. **Run the application**
   ```bash
   python manage.py runserver
   ```

## Configuration

### MongoDB Setup
1. Install MongoDB on your system
2. Start MongoDB service
3. Update `MONGO_URI` in your `.env` file

### Razorpay Setup
1. Create a Razorpay account at https://razorpay.com
2. Get your API keys from the dashboard
3. Update `RAZORPAY_KEY_ID` and `RAZORPAY_KEY_SECRET` in your `.env` file

## Usage

### Student Workflow
1. **Registration**: Students register with college ID, email, and personal details
2. **Login**: Login using college ID and password
3. **Dashboard**: View profile and available fee payment options
4. **Payment**: Select fee type and pay using Razorpay
5. **Receipt**: Download PDF receipt after successful payment

### Admin Workflow
1. **Login**: Admin login with username and password
2. **Dashboard**: View system statistics and recent activities
3. **Student Management**: View, search, and manage student accounts
4. **Fee Management**: Update fee amounts for students
5. **Monitoring**: Track payments and generate reports

## API Endpoints

### Student APIs
- `POST /students/register/` - Student registration
- `POST /students/login/` - Student login
- `GET /students/dashboard/` - Student dashboard
- `GET /students/profile/` - Student profile
- `GET /students/payment-history/` - Payment history

### Payment APIs
- `POST /payments/create-order/` - Create Razorpay order
- `POST /payments/verify-payment/` - Verify payment signature
- `GET /payments/download-receipt/<id>/` - Download receipt

### Admin APIs
- `POST /admins/login/` - Admin login
- `GET /admins/dashboard/` - Admin dashboard
- `GET /admins/students/` - Students list
- `POST /admins/students/<id>/fees/` - Update student fees

## Database Schema

### Student Model
- College ID (unique)
- Email (unique)
- Full Name
- Phone Number
- Profile Picture
- Admission Type (Counseling/Management)
- Fee Amounts (College, Exam, Bus)

### Payment Model
- Student (Foreign Key)
- Fee Type
- Amount
- Razorpay Order/Payment IDs
- Status
- Receipt Number

### Admin Model
- Username (unique)
- Email (unique)
- Full Name
- Password (hashed)
- Super Admin flag

## Security Features

- Password hashing using Django's built-in hashers
- CSRF protection on all forms
- Session-based authentication
- Razorpay signature verification
- Input validation and sanitization
- SQL injection prevention through ORM

## Deployment

### Production Settings
1. Set `DEBUG=False` in production
2. Configure proper `ALLOWED_HOSTS`
3. Use environment variables for sensitive data
4. Set up proper MongoDB authentication
5. Configure email settings for notifications
6. Set up SSL/HTTPS for secure payments

### Static Files
```bash
python manage.py collectstatic
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For support and questions, please contact the development team or create an issue in the repository.