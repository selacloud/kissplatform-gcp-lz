#
AR_REPO='gemini-repo'
SERVICE_NAME='gemini-streamlit-app' 
gcloud artifacts repositories create "$AR_REPO" --location="$GCP_REGION" --repository-format=Docker
gcloud builds submit --tag "$GCP_REGION-docker.pkg.dev/$GCP_PROJECT/$AR_REPO/$SERVICE_NAME"

export GCP_PROJECT='kisspf-stakeholder-sl-dev-0'
export GCP_REGION='us-east1'

streamlit run app.py \
  --browser.serverAddress=localhost \
  --server.enableCORS=false \
  --server.enableXsrfProtection=false \
  --server.port 8080

streamlit run FH_stakeholder.py \
    --browser.serverAddress=localhost \
    --server.enableCORS=false \
    --server.enableXsrfProtection=false \
    --server.port 8080
