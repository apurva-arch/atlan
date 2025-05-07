"""
Authentication Service for Atlan Integration

This service handles authentication with the Atlan API, including:
- OAuth 2.0 authentication
- API key authentication
- Token management
- User authentication
"""

import os
import time
import logging
import requests
from datetime import datetime, timedelta
from flask import current_app

logger = logging.getLogger(__name__)

class AuthService:
    """
    Service for handling authentication with Atlan API
    """
    
    def __init__(self, config):
        """
        Initialize the authentication service
        
        Args:
            config: Application configuration
        """
        self.config = config
        self.api_url = config.get('ATLAN_API_URL')
        self.api_key = config.get('ATLAN_API_KEY')
        self.client_id = config.get('ATLAN_CLIENT_ID')
        self.client_secret = config.get('ATLAN_CLIENT_SECRET')
        
        # Token cache
        self._access_token = None
        self._token_expiry = None
        self._refresh_token = None
        
        logger.info("Authentication service initialized")
    
    def get_access_token(self):
        """
        Get a valid access token, refreshing if necessary
        
        Returns:
            str: Access token
        """
        # If we have a valid token, return it
        if self._access_token and self._token_expiry and datetime.now() < self._token_expiry:
            return self._access_token
        
        # If we have a refresh token, try to use it
        if self._refresh_token:
            try:
                self._refresh_access_token()
                return self._access_token
            except Exception as e:
                logger.warning(f"Failed to refresh token: {e}")
        
        # Otherwise, get a new token
        self._get_new_access_token()
        return self._access_token
    
    def _get_new_access_token(self):
        """
        Get a new access token using client credentials
        
        Raises:
            Exception: If authentication fails
        """
        logger.info("Getting new access token")
        
        url = f"{self.api_url.split('/api')[0]}/oauth/token"
        
        payload = {
            'grant_type': 'client_credentials',
            'client_id': self.client_id,
            'client_secret': self.client_secret
        }
        
        try:
            response = requests.post(url, data=payload)
            response.raise_for_status()
            
            data = response.json()
            self._access_token = data.get('access_token')
            self._refresh_token = data.get('refresh_token')
            
            # Calculate token expiry time
            expires_in = data.get('expires_in', 3600)
            self._token_expiry = datetime.now() + timedelta(seconds=expires_in)
            
            logger.info("Successfully obtained new access token")
        except requests.exceptions.RequestException as e:
            logger.error(f"Failed to get access token: {e}")
            raise Exception(f"Authentication failed: {e}")
    
    def _refresh_access_token(self):
        """
        Refresh the access token using the refresh token
        
        Raises:
            Exception: If token refresh fails
        """
        logger.info("Refreshing access token")
        
        url = f"{self.api_url.split('/api')[0]}/oauth/token"
        
        payload = {
            'grant_type': 'refresh_token',
            'refresh_token': self._refresh_token,
            'client_id': self.client_id,
            'client_secret': self.client_secret
        }
        
        try:
            response = requests.post(url, data=payload)
            response.raise_for_status()
            
            data = response.json()
            self._access_token = data.get('access_token')
            self._refresh_token = data.get('refresh_token')
            
            # Calculate token expiry time
            expires_in = data.get('expires_in', 3600)
            self._token_expiry = datetime.now() + timedelta(seconds=expires_in)
            
            logger.info("Successfully refreshed access token")
        except requests.exceptions.RequestException as e:
            logger.error(f"Failed to refresh token: {e}")
            raise Exception(f"Token refresh failed: {e}")
    
    def get_headers(self):
        """
        Get headers for API requests, including authentication
        
        Returns:
            dict: Headers for API requests
        """
        headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        }
        
        # Use API key if available, otherwise use OAuth token
        if self.api_key:
            headers['X-Atlan-API-Key'] = self.api_key
        else:
            headers['Authorization'] = f"Bearer {self.get_access_token()}"
        
        return headers
    
    def authenticate_user(self, username, password):
        """
        Authenticate a user with username and password
        
        Args:
            username (str): User's username
            password (str): User's password
            
        Returns:
            dict: User information and tokens
            
        Raises:
            Exception: If authentication fails
        """
        logger.info(f"Authenticating user: {username}")
        
        url = f"{self.api_url.split('/api')[0]}/oauth/token"
        
        payload = {
            'grant_type': 'password',
            'username': username,
            'password': password,
            'client_id': self.client_id,
            'client_secret': self.client_secret
        }
        
        try:
            response = requests.post(url, data=payload)
            response.raise_for_status()
            
            data = response.json()
            
            # Get user information
            user_info = self.get_user_info(data.get('access_token'))
            
            return {
                'access_token': data.get('access_token'),
                'refresh_token': data.get('refresh_token'),
                'expires_in': data.get('expires_in'),
                'user': user_info
            }
        except requests.exceptions.RequestException as e:
            logger.error(f"User authentication failed: {e}")
            raise Exception(f"Authentication failed: {e}")
    
    def get_user_info(self, token=None):
        """
        Get information about the authenticated user
        
        Args:
            token (str, optional): Access token. If not provided, the service token will be used.
            
        Returns:
            dict: User information
            
        Raises:
            Exception: If the request fails
        """
        logger.info("Getting user information")
        
        url = f"{self.api_url.split('/api')[0]}/api/v2/users/current"
        
        headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        }
        
        if token:
            headers['Authorization'] = f"Bearer {token}"
        else:
            headers['Authorization'] = f"Bearer {self.get_access_token()}"
        
        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"Failed to get user info: {e}")
            raise Exception(f"Failed to get user information: {e}")
    
    def validate_token(self, token):
        """
        Validate an access token
        
        Args:
            token (str): Access token to validate
            
        Returns:
            bool: True if the token is valid, False otherwise
        """
        logger.info("Validating token")
        
        url = f"{self.api_url.split('/api')[0]}/api/v2/users/current"
        
        headers = {
            'Authorization': f"Bearer {token}"
        }
        
        try:
            response = requests.get(url, headers=headers)
            return response.status_code == 200
        except:
            return False
