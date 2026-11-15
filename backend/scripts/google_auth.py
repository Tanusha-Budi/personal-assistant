from google_auth_oauthlib.flow import InstalledAppFlow

from app.config import settings
from app.services.google_auth import SCOPES


def main():
    flow = InstalledAppFlow.from_client_secrets_file(
        settings.google_credentials_path, SCOPES
    )
    creds = flow.run_local_server(port=0)
    with open(settings.google_token_path, "w") as f:
        f.write(creds.to_json())
    print("Saved token to", settings.google_token_path)


if __name__ == "__main__":
    main()