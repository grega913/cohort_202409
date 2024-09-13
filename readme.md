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
   (2. optional) - to see if the docker works ok: docker run -d -p 8501:8501 cohort_202409
2. docker tag cohort_202409 europe-west1-docker.pkg.dev/ai01-51d16/cohort/cohort_202409:latest
3. docker push europe-west1-docker.pkg.dev/ai01-51d16/cohort/cohort_202409:latest

## 20240910

- Docker working locally. There were some issues with dotenv, but solved now.
- Streamlit working locally and also in local docker
- Trying to deploy to Artifact Registry on GCP, but on a Project named ai01, not on Besistem, following this guy: https://www.youtube.com/watch?v=MM4viHa7k4w&ab_channel=ScriptBytes

\*\* Container Registry is deprecated . . moving to Artifact Registry
https://cloud.google.com/artifact-registry/docs/transition/transition-from-gcr
