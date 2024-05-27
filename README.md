Welcome to the GenAI-related code challenge for a full-stack developer. It's involves creating a simple web application that integrates an AI model to provide a sentimental analyses. 

## Objective
Develop a web application that allows users to input text and receive a sentiment analysis score (positive, negative, neutral) using a pre-trained AI model.

## Backend
Create a user interface with a **text input box** and a **submit button**.
Display the sentiment score and a **textual** sentiment (e.g., "Positive", "Negative", "Neutral") upon submission

Set up a POST REST API endpoint to handle the sentiment analysis requests.
Integrate a pre-trained sentiment analysis model (e.g., from Hugging Face's Transformers library or any other API like Google Cloud Natural Language API)

### Technical Specifications
Use the `app` solution folder to include the source code with .NET 6+ (Preferencial) or Node.js with Express.
Ensure to allow anonymous connection in CORS and receive data with `application/json`.

### Deployment
Deploy the application on a cloud platform (e.g., Heroku)

## Data Flow:
The frontend should send the user's text input to the backend via a **POST** request.
The backend should process this input using the sentiment analysis model and **return the results** to the frontend.

## Definition of Done
1. Nanoservice with a endpoint to provide sentimental analyses.
2. Deployed and acessible via public URL.
3. Open-API documentation (a.k.a swagger) of the exposed API.
4. Communication stablished with the frontend.
