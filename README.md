# Sahara - AI Mental Wellness Ally

Sahara is an AI-powered, confidential, and empathetic mental wellness chatbot designed to support the youth in India. It provides a safe, anonymous, and non-judgmental space for users to take the first step in their mental wellness journey, helping to overcome stigma and access support.

This project was built for a hackathon, focusing on creating a scalable, responsible, and impactful prototype using Google Cloud's generative AI technologies.

✨ Vision & Mission
Mental health remains a significant challenge for young adults in India, who often face intense academic and social pressures without a confidential outlet. Our mission is to bridge this gap by providing an accessible "stigma-free front door" to mental wellness. Sahara is not a replacement for professional therapy but serves as a supportive first point of contact, offering empathetic conversation and a critical safety net for users in distress.

🚀 Key Features
Empathetic Conversational AI: Built on Google's Dialogflow CX, Sahara engages in natural, supportive conversations, avoiding robotic scripts.

Critical Safety System: A robust, two-stage crisis detection module scans every message for high-risk language related to self-harm, suicide, or abuse.

Immediate Escalation: When a crisis is detected, the system immediately provides contact information for verified Indian mental health helplines like Tele MANAS (14416) and the Vandrevala Foundation.

Calming & Accessible UI: The user interface is designed to be minimalist and soothing, reducing cognitive load for users who may be in distress.

Serverless & Scalable: The entire application is built on a serverless architecture using Cloud Run and Firebase Hosting, ensuring it can scale efficiently and cost-effectively.   

🛠️ Tech Stack
The project is divided into two main components: a Python backend and a static web frontend.

Frontend:

HTML5

(https://tailwindcss.com/) - A utility-first CSS framework.

daisyUI - A component library for Tailwind CSS for beautiful, calming UI elements.   

Backend:

Python 3.11+

Flask - A lightweight web framework for the API server.   

Gunicorn - A production-ready WSGI server.

Cloud & AI Services:

(https://cloud.google.com/run): Hosts the serverless Python backend.   

Firebase Hosting: Deploys and hosts the frontend on a global CDN.   

(https://cloud.google.com/dialogflow/cx/docs): The core conversational agent for managing dialogue flows and understanding user intent.

🏗️ Architecture Overview
The application follows a simple, decoupled architecture:

User Interface (Firebase Hosting): The user interacts with a static HTML/CSS/JS single-page application.

API Request: The frontend sends the user's message to the backend API.

Backend Logic (Cloud Run): The Flask server receives the request.

It first runs the message through the Crisis Detection module.

If a crisis is detected, it immediately returns a safety response.

If no crisis is detected, it forwards the message to the Dialogflow CX agent.

Conversational AI (Dialogflow CX): The agent processes the message, matches an intent (like the welcome intent), and returns a pre-configured response.

API Response: The backend sends the agent's response back to the frontend, which displays it to the user.

⚙️ Getting Started: Setup and Deployment
Follow these steps to set up and run the project.

Prerequisites
A Google Cloud Project with billing enabled (required to activate free tiers and credits).

Google Cloud CLI installed and authenticated (gcloud auth login).

Python 3.9+ installed.

Node.js and npm installed (for the Firebase CLI).

1. Google Cloud Configuration
First, set up your Google Cloud project and enable the necessary APIs.bash

Set your project ID (replace YOUR_PROJECT_ID)
gcloud config set project YOUR_PROJECT_ID

Enable all required services
gcloud services enable

https://www.google.com/search?q=dialogflow.googleapis.com

run.googleapis.com

artifactregistry.googleapis.com

cloudbuild.googleapis.com

https://www.google.com/search?q=aiplatform.googleapis.com

https://www.google.com/search?q=firebasehosting.googleapis.com


### 2. Dialogflow CX Agent Setup

Create the conversational agent that will power the chatbot.

1.  **Go to the(https://dialogflow.cloud.google.com/cx/)**.
2.  Click **Create agent** > **Build your own**.
3.  Set the **Display name** to `sahara-agent`.
4.  Select a **Location** (e.g., `us-central1`). **Remember this location!**
5.  Click **Save**.
6.  In the agent's **Build** tab, click the **Start** page, then the **Default Welcome Intent** route.
7.  Under **Fulfillment**, add an empathetic welcome message like: `Hello! I'm Sahara, your AI companion. I'm here to listen and support you in a safe, non-judgmental space. How are you feeling today?`
8.  **Save** the changes.
9.  **Copy the Agent ID:** Click the three-dot menu next to your agent's name and select **Copy name**. The ID is the last part of the string (e.g., `.../agents/AGENT_ID`).

### 3. Backend Deployment

Deploy the Python Flask server to Cloud Run.

1.  Navigate to the `backend` directory.
2.  Run the deployment command. Replace the placeholders with your actual values. Use the same region you chose for your Dialogflow agent.

    ```bash
    gcloud run deploy sahara-backend \
      --source. \
      --platform managed \
      --region YOUR_GCP_REGION \
      --allow-unauthenticated \
      --min-instances=0 \
      --set-env-vars="GCP_PROJECT_ID=YOUR_PROJECT_ID,DF_LOCATION=YOUR_GCP_REGION,DF_AGENT_ID=YOUR_AGENT_ID"
    ```
    *   `--min-instances=0` ensures the service scales to zero to stay within the free tier.

3.  After deployment, the command will output a **Service URL**. Copy this URL.

### 4. Frontend Deployment

Deploy the user-facing web app to Firebase Hosting.

1.  **Update the Backend URL:** Open `frontend/index.html` and replace `YOUR_CLOUD_RUN_SERVICE_URL_HERE` with the Service URL you just copied.
2.  **Install Firebase CLI:**
    ```bash
    npm install -g firebase-tools
    ```
3.  **Initialize Firebase:** Navigate to the `frontend` directory and run:
    ```bash
    firebase login
    firebase init hosting
    ```
    *   Follow the prompts:
        *   Select **Use an existing project** and choose your GCP project.
        *   Set your public directory to **`.`** (a single dot).
        *   Configure as a single-page app: **Yes**.
        *   Set up automatic builds with GitHub: **No**.

4.  **Deploy the frontend:**
    ```bash
    firebase deploy --only hosting
    ```

5.  The command will output a **Hosting URL**. Open this URL in your browser to chat with Sahara!

## ⚖️ Ethical Considerations

This project handles potentially sensitive conversations, and safety is the top priority.

*   **Not a Replacement for Therapy:** The chatbot is explicitly designed as a supportive tool, not a clinical replacement. It always encourages professional help for serious issues.
*   **Crisis Management:** The keyword-based crisis detection system is a critical safeguard designed to immediately route users expressing high-risk thoughts to verified, professional helplines.
*   **Data Privacy:** The current prototype does not store conversation logs. Any future development involving data persistence must adhere to strict privacy laws like HIPAA and India's DPDP Act.
*   **Transparency:** The UI clearly states that the user is interacting with an AI.

## 🗺️ Future Roadmap

This hackathon prototype sets the foundation for a more powerful wellness tool. Future enhancements could include:

*   **Generative AI Responses:** Integrate Google's Gemini API via the backend webhook to provide more dynamic, context-aware, and empathetic responses instead of static ones.
*   **Database Integration:** Use Firestore to allow users to optionally save their conversation history, track their mood over time, and maintain a private journal.
*   **Guided Exercises:** Create dedicated Dialogflow CX flows for evidence-based techniques like Cognitive Behavioral Therapy (CBT) exercises, mindfulness, and breathing practices.
*   **Personalized Journeys:** Leverage AI to analyze a user's (anonymized and consented) history to suggest personalized wellness plans and resources.

## 📄 License

This project is licensed under the MIT License. See the `LICENSE` file for details.
