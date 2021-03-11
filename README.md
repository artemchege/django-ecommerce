What is it all about: 
this is the e-commerce site where user can buy items (both that require shipping and not).
Moreover user may do shopping without any registration (sessions key used). 

![Main page example](mainpage.png "mainpage")

Used technologies:
1. Bootstrap.
2. jQuery ajax.
3. Signals.
4. Selenium.
5. PostgreSQL integration: Amazon web services (AWS). 
6. AWS S3 integration for static files. 
7. Stripe as payment system.
8. Whitenoise + gunicorn.
9. Heroku config.
10. Dockerfile.

Coming improvements:

1. More tests.
2. Admin panel improvements (customization).

How to run: 

1. Сonfigure your SMPT credentials (gmail config) in .env file in ecommerce folder. 
Required variables:
- EMAIL_HOST_USER=your_email
- EMAIL_HOST_PASSWORD=your_password

In case you are going to use Amazon services: 
- AWS_USER=your_data
- AWS_PASSWORD=your_data
- AWS_PORT=your_data
- AWS_HOST=your_data
- AWS_ACCESS_KEY_ID=your_data
- AWS_SECRET_ACCESS_KEY=your_data

Stripe secret_key:
- STRIPE_SECRET_KEY=your_key
2. Edit ALLOWED_HOST = []
3. Run in command line: 

    git clone https://github.com/artemchege/django-ecommerce .

4. Then run (Windows compatible): 

    python manage.py runserver 
    
5. Or in Docker: 

    git clone https://github.com/artemchege/django-ecommerce .
    
    docker build -t django-ecommerce 
    
    Then if Django dev server:
    
    docker run -p 8001:8001 -e EMAIL_HOST_USER=your_data
                            -e EMAIL_HOST_PASSWORD=your data
                            -e AWS_USER=your_data
                            -e AWS_PASSWORD=your_data
                            -e AWS_PORT=your_data
                            -e AWS_HOST=your_data
                            -e AWS_ACCESS_KEY_ID=your_data
                            -e AWS_SECRET_ACCESS_KEY=your_data
                            -e STRIPE_SECRET_KEY=your_data
    django-ecommerce -d python manage.py runserver 0.0.0.0:8001 
                            
    Or if gunicorn server: 
    
    docker run -p 8001:8001 -e EMAIL_HOST_USER=your_data
                        -e EMAIL_HOST_PASSWORD=your data
                        -e AWS_USER=your_data
                        -e AWS_PASSWORD=your_data
                        -e AWS_PORT=your_data
                        -e AWS_HOST=your_data
                        -e AWS_ACCESS_KEY_ID=your_data
                        -e AWS_SECRET_ACCESS_KEY=your_data
                        -e STRIPE_SECRET_KEY=your_data
    django-ecommerce -d gunicorn --bind 0.0.0.0:8001 --workers 3 ecommerce.wsgi
                        
    
Deployed on Heroku: https://ecommerce-pure-django.herokuapp.com/

(!) On heroku Stripe confirmation does not work because there is no SSL configured on due to free heroku plan. 
