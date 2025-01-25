# Discord oAuth2 Bot

This project is divided into two main components. Here is what each component does:

## Flask API

-   /callback - Handles incoming oAuth2 requests and if the authentication is successful -> logs that user's **email and IP address** through the provided webhook (see example_config.py) -> saves into the database
-   /api/users - Lets the Discord Bot fetch, update and remove authenticated users in the database

## Discord bot

-   Dynamically generates an oAuth2 URL (command: /oauth2)
-   Listens for MEMBER_REMOVE events through Discord's WebSocket API.
-   Detects an authenticated user leaving the server -> immediately refreshes that user's access/refresh token (if expired) and makes them join the server back.

### Setup support
- My Discord: @packslasher
- My Telegram @coinise
