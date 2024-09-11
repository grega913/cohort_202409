# [Code and description for Alejandro's Cohort by GS](https://course.alejandro-ao.com/)

Code for Alejandro's Cohort
Most examples are on gDrive.
This is version for deployment -> added Streamlit for WEB.

#### Deploy to google's Artifact Registry

check if you are in the right project - ai01 in my case -

gcloud projects list


1. docker build -t my_streamlit .
2. docker tag my_streamlit europe-west1-docker.pkg.dev/ai01-51d16/my-streamlit/my_streamlit:latest
3. docker push europe-west1-docker.pkg.dev/ai01-51d16/my-streamlit/my_streamlit:latest





## 20240910

- Docker working locally. There were some issues with dotenv, but solved now.
- Streamlit working locally and also in local docker
- Trying to deploy to Artifact Registry on GCP, but on a Project named ai01, not on Besistem, following this guy: https://www.youtube.com/watch?v=MM4viHa7k4w&ab_channel=ScriptBytes

\*\* Container Registry is deprecated . . moving to Artifact Registry
https://cloud.google.com/artifact-registry/docs/transition/transition-from-gcr


