import dropbox


def get_refresh_token(APP_KEY, APP_SECRET):
    auth_flow = dropbox.DropboxOAuth2FlowNoRedirect(APP_KEY, APP_SECRET, token_access_type="offline")
    authorize_url = auth_flow.start()

    print("1. Acesse:", authorize_url)
    print("2. Clique em 'Permitir'")
    print("3. Copie o código gerado e cole aqui:")

    auth_code = input("Cole o código aqui: ").strip()
    oauth_result = auth_flow.finish(auth_code)

    print("Access Token:", oauth_result.access_token)
    print("Refresh Token:", oauth_result.refresh_token)
    print("App Key:", APP_KEY)
    print("App Secret:", APP_SECRET)