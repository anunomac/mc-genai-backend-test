
# Django + Celery Setup    
    
This repository contains the setup for a Django project integrated with Celery for asynchronous task processing. The project also uses RabbitMQ as the message broker.    
    
## Table of Contents    
 - [Requirements](#requirements)    
- [Installation](#installation)    
- [Running the Project](#running-the-project)    
- [API documentation](#api-documentation) 
    
## Requirements    
 - Python 3.x    
- Django    
- Celery    
- RabbitMQ    
- Docker (optional, for RabbitMQ container)    
- Other python requirements provided in requirements.txt  
    
## Installation    
 ### 1. Clone the Repository    
 ```bash
 git clone https://github.com/anunomac/mc-genai-backend-test.git cd yourrepository
 ```   
 ### 2. Create a Virtual Environment    
 ```bash
 python -m venv venv
 source venv/bin/activate  # On Windows use `venv\Scripts\activate`
  ```   
 ### 3. Install Dependencies    
 ```bash
 pip install -r requirements.txt
 ```   
 ### 4. Install RabbitMQ    
 #### Option 1: Using Docker    
 ```bash
 docker run -d --name rabbitmq -p 5672:5672 -p 15672:15672 rabbitmq:management
 ```   
 #### Option 2: Manual Installation    
 Follow the installation guide on the [RabbitMQ website](https://www.rabbitmq.com/download.html).    
  
    
## Running the Project
Note: using celery/rabbitMQ is not mandatory, simply replace function calls for their SYNC version.  
    
### 1. Start RabbitMQ    
 If you are using Docker:    
    
```bash
docker start rabbitmq
```   
 If you installed RabbitMQ manually, ensure it is running.    
    
### 2. Run Django Migrations    
 ```bash
 python manage.py makemigrations python manage.py migrate
 ```   
 ### 3. Start Django Development Server    
 ```bash
 python manage.py runserver
 ```   
 ### 4. Start Celery Worker    
 ```bash
 celery -A SentimentAnalyzer worker --loglevel=INFO -P solo #-P solo is sometimes required on windows due to concurrency/threading problems
 ```   

 ## API documentation    
 ### Initiate a Sentiment Analysis    
 Use the provided API endpoints to initiate a sentiment analysis.    
    
#### Example Request    
 ```bash
 POST /classifications/
  {    
 "query": "Your text here",    
 "model": 1
 }
 ```   
 ### Check Classification Status    
 Use the provided API endpoint to check the classification status.    
    
#### Example Request    
 ```
  GET /classifications/?cid=<classification_id>&access_key=<access_key>
  ```   

### OpenAPI documentation
The API documentation for this project is available in OpenAPI format and can be accessed via Swagger UI or ReDoc.  
  
### Accessing the Documentation
  
- **Swagger UI**: [http://127.0.0.1:8000/swagger/](http://127.0.0.1:8000/swagger/)  
- **ReDoc**: [http://127.0.0.1:8000/redoc/](http://127.0.0.1:8000/redoc/)  
- **OpenAPI JSON**: [http://127.0.0.1:8000/swagger.json](http://127.0.0.1:8000/swagger.json)  
- **OpenAPI YAML**: [http://127.0.0.1:8000/swagger.yaml](http://127.0.0.1:8000/swagger.yaml)
### Additional Resources    
    
- [Celery Documentation](https://docs.celeryproject.org/)    
- [Django Documentation](https://docs.djangoproject.com/)    
- [RabbitMQ Documentation](https://www.rabbitmq.com/documentation.html)