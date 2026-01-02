import requests
import getpass

client_id = input('Enter your Twitch Client ID: ')
client_secret = getpass.getpass('Enter your Twitch Client Secret: ')
redirect_uri = input('Enter your Redirect URI (e.g. http://localhost:3000): ')
code = input('Enter the authorization code from Twitch: ')

token_url = 'https://id.twitch.tv/oauth2/token'
payload = {
    'client_id': client_id,
    'client_secret': client_secret,
    'code': code,
    'grant_type': 'authorization_code',
    'redirect_uri': redirect_uri
}

print('Requesting new OAuth token from Twitch...')
response = requests.post(token_url, data=payload)

if response.status_code == 200:
    data = response.json()
    print('\nYour new OAuth token:')
    print(data['access_token'])
    print(f"\nRefresh token: {data.get('refresh_token', 'N/A')}")
    print(f"Token type: {data['token_type']}")
    print(f"Expires in: {data['expires_in']} seconds")
else:
    print('Failed to get token:')
    print(response.status_code, response.text)
