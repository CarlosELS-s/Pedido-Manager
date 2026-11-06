from google_auth_oauthlib.flow import InstalledAppFlow

SCOPES = [
    "https://www.googleapis.com/auth/gmail.send"
]

flow = InstalledAppFlow.from_client_secrets_file(
    "credentials.json",
    SCOPES
)

print("Abrindo autorização do Google...")

credentials = flow.run_local_server(
    host="127.0.0.1",
    port=8080,
    access_type="offline",
    prompt="consent",
    open_browser=True
)

print("\nAutorização concluída!")
print("\nREFRESH TOKEN:")
print(credentials.refresh_token)