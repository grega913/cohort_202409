# Added Lesson 8

## Lesson 8, Topic 6 - 20241002 - https://app.alejandro-ao.com/topics/lab-onboarding-assistant/

1. Exercise: Build an Onboarding Assistant for the Umbrella Corporation - Alejandro's Repo: https://github.com/alejandro-ao/U2qfZneHGMNTNEw
2. My version is in "lessons/l8_onboarding_assistant_gs.py"
3. Alejandro's version is in "lessons/l8_onboarding_assistant_alejandro.py" - Lesson8, Topic7: https://app.alejandro-ao.com/topics/rag-lab-solution/

3.1 making assistant class -> assumimg we are not gonna be using streamlit
3.2 Assistant class creates a RAG chain
3.3 message history and employee information are dealt with streamlit session state
3.4 GUI with Streamlit->idea is to pass Assistant as a dependency to Streamlit model
3.5 render methods -> rendering main parts of apps
3.6 run the app with "streamlit run src/lessons/lesson8/l8_onboarding_assistant_Alejandro.py"

# Added Lesson 7

## Lesson 7, Topic 10 - 20240927 - https://app.alejandro-ao.com/topics/project-your-gui-ai-assistant/

1.  Building a GUI AI Assistant with memory with Streamlit
2.  located at: src\lessons\lesson7_project_gui.py
3.  main points:
    - storing messages into st.session_state
    - creating a function that returns chat_with_message_history, using RunnableWithMessageHistory
    - decorating the function with @st.cache_resource as ChatHistory is defined within function
    -

# [Code and description for Alejandro's Cohort by GS](https://course.alejandro-ao.com/)

Code for Alejandro's Cohort
Most examples are on gDrive.
This is version for deployment -> added Streamlit for WEB.

#### Deploy to google's Artifact Registry

check if you are in the right project - ai01 in my case -
gcloud projects list
make sure repo exist in specified location on gcloud
check last line in the docker for the starting file

1. docker build -t cohort_202409 .
   (2. optional) - to see if the docker works ok: docker run -d -p 80:8080 cohort_202409
2. docker tag cohort_202409 europe-west1-docker.pkg.dev/ai01-51d16/cohort/cohort_202409:latest
3. docker push europe-west1-docker.pkg.dev/ai01-51d16/cohort/cohort_202409:latest

## 20240910

- Docker working locally. There were some issues with dotenv, but solved now.
- Streamlit working locally and also in local docker
- Trying to deploy to Artifact Registry on GCP, but on a Project named ai01, not on Besistem, following this guy: https://www.youtube.com/watch?v=MM4viHa7k4w&ab_channel=ScriptBytes

\*\* Container Registry is deprecated . . moving to Artifact Registry
https://cloud.google.com/artifact-registry/docs/transition/transition-from-gcr
