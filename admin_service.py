"""
Admin Service for Atlan Integration

This service handles administrative operations in Atlan, including:
- User management
- Group management
- Workspace configuration
- Audit logs
- Usage metrics
"""

import logging
import requests
import json
from flask import current_app

logger = logging.getLogger(__name__)

class AdminService:
    """
    Service for handling Atlan administrative operations
    """
    
    def __init__(self, config, auth_service):
        """
        Initialize the admin service
        
        Args:
            config: Application configuration
            auth_service: Authentication service
        """
        self.config = config
        self.auth_service = auth_service
        self.api_url = config.get('ATLAN_API_URL')
        
        logger.info("Admin service initialized")
    
    def get_users(self, limit=10, offset=0, sort_by=None, order=None, filter_expr=None):
        """
        Get a list of users
        
        Args:
            limit (int): Maximum number of users to return
            offset (int): Offset for pagination
            sort_by (str): Field to sort by
            order (str): Sort order ('asc' or 'desc')
            filter_expr (str): Filter expression
            
        Returns:
            dict: List of users and pagination information
            
        Raises:
            Exception: If the request fails
        """
        logger.info(f"Getting users (limit={limit}, offset={offset})")
        
        url = f"{self.api_url}/users"
        
        params = {
            'limit': limit,
            'offset': offset
        }
        
        if sort_by:
            params['sort'] = sort_by
        
        if order:
            params['order'] = order
        
        if filter_expr:
            params['filter'] = filter_expr
        
        try:
            response = requests.get(
                url,
                params=params,
                headers=self.auth_service.get_headers()
            )
            response.raise_for_status()
            
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"Failed to get users: {e}")
            raise Exception(f"Failed to get users: {e}")
    
    def get_user(self, user_id):
        """
        Get a user by ID
        
        Args:
            user_id (str): User ID
            
        Returns:
            dict: User details
            
        Raises:
            Exception: If the request fails
        """
        logger.info(f"Getting user with ID: {user_id}")
        
        url = f"{self.api_url}/users/{user_id}"
        
        try:
            response = requests.get(
                url,
                headers=self.auth_service.get_headers()
            )
            response.raise_for_status()
            
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"Failed to get user: {e}")
            raise Exception(f"Failed to get user: {e}")
    
    def create_user(self, user_data):
        """
        Create a new user
        
        Args:
            user_data (dict): User data
            
        Returns:
            dict: Created user
            
        Raises:
            Exception: If the request fails
        """
        logger.info(f"Creating user: {user_data.get('username')}")
        
        url = f"{self.api_url}/users"
        
        try:
            response = requests.post(
                url,
                json=user_data,
                headers=self.auth_service.get_headers()
            )
            response.raise_for_status()
            
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"Failed to create user: {e}")
            raise Exception(f"Failed to create user: {e}")
    
    def update_user(self, user_id, user_data):
        """
        Update a user
        
        Args:
            user_id (str): User ID
            user_data (dict): Updated user data
            
        Returns:
            dict: Updated user
            
        Raises:
            Exception: If the request fails
        """
        logger.info(f"Updating user with ID: {user_id}")
        
        url = f"{self.api_url}/users/{user_id}"
        
        try:
            response = requests.put(
                url,
                json=user_data,
                headers=self.auth_service.get_headers()
            )
            response.raise_for_status()
            
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"Failed to update user: {e}")
            raise Exception(f"Failed to update user: {e}")
    
    def delete_user(self, user_id):
        """
        Delete a user
        
        Args:
            user_id (str): User ID
            
        Returns:
            dict: Deletion status
            
        Raises:
            Exception: If the request fails
        """
        logger.info(f"Deleting user with ID: {user_id}")
        
        url = f"{self.api_url}/users/{user_id}"
        
        try:
            response = requests.delete(
                url,
                headers=self.auth_service.get_headers()
            )
            response.raise_for_status()
            
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"Failed to delete user: {e}")
            raise Exception(f"Failed to delete user: {e}")
    
    def get_groups(self, limit=10, offset=0):
        """
        Get a list of groups
        
        Args:
            limit (int): Maximum number of groups to return
            offset (int): Offset for pagination
            
        Returns:
            dict: List of groups and pagination information
            
        Raises:
            Exception: If the request fails
        """
        logger.info(f"Getting groups (limit={limit}, offset={offset})")
        
        url = f"{self.api_url}/groups"
        
        params = {
            'limit': limit,
            'offset': offset
        }
        
        try:
            response = requests.get(
                url,
                params=params,
                headers=self.auth_service.get_headers()
            )
            response.raise_for_status()
            
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"Failed to get groups: {e}")
            raise Exception(f"Failed to get groups: {e}")
    
    def get_group(self, group_id):
        """
        Get a group by ID
        
        Args:
            group_id (str): Group ID
            
        Returns:
            dict: Group details
            
        Raises:
            Exception: If the request fails
        """
        logger.info(f"Getting group with ID: {group_id}")
        
        url = f"{self.api_url}/groups/{group_id}"
        
        try:
            response = requests.get(
                url,
                headers=self.auth_service.get_headers()
            )
            response.raise_for_status()
            
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"Failed to get group: {e}")
            raise Exception(f"Failed to get group: {e}")
    
    def create_group(self, group_data):
        """
        Create a new group
        
        Args:
            group_data (dict): Group data
            
        Returns:
            dict: Created group
            
        Raises:
            Exception: If the request fails
        """
        logger.info(f"Creating group: {group_data.get('name')}")
        
        url = f"{self.api_url}/groups"
        
        try:
            response = requests.post(
                url,
                json=group_data,
                headers=self.auth_service.get_headers()
            )
            response.raise_for_status()
            
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"Failed to create group: {e}")
            raise Exception(f"Failed to create group: {e}")
    
    def update_group(self, group_id, group_data):
        """
        Update a group
        
        Args:
            group_id (str): Group ID
            group_data (dict): Updated group data
            
        Returns:
            dict: Updated group
            
        Raises:
            Exception: If the request fails
        """
        logger.info(f"Updating group with ID: {group_id}")
        
        url = f"{self.api_url}/groups/{group_id}"
        
        try:
            response = requests.put(
                url,
                json=group_data,
                headers=self.auth_service.get_headers()
            )
            response.raise_for_status()
            
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"Failed to update group: {e}")
            raise Exception(f"Failed to update group: {e}")
    
    def delete_group(self, group_id):
        """
        Delete a group
        
        Args:
            group_id (str): Group ID
            
        Returns:
            dict: Deletion status
            
        Raises:
            Exception: If the request fails
        """
        logger.info(f"Deleting group with ID: {group_id}")
        
        url = f"{self.api_url}/groups/{group_id}"
        
        try:
            response = requests.delete(
                url,
                headers=self.auth_service.get_headers()
            )
            response.raise_for_status()
            
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"Failed to delete group: {e}")
            raise Exception(f"Failed to delete group: {e}")
    
    def add_user_to_group(self, user_id, group_id):
        """
        Add a user to a group
        
        Args:
            user_id (str): User ID
            group_id (str): Group ID
            
        Returns:
            dict: Operation status
            
        Raises:
            Exception: If the request fails
        """
        logger.info(f"Adding user {user_id} to group {group_id}")
        
        url = f"{self.api_url}/groups/{group_id}/users/{user_id}"
        
        try:
            response = requests.post(
                url,
                headers=self.auth_service.get_headers()
            )
            response.raise_for_status()
            
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"Failed to add user to group: {e}")
            raise Exception(f"Failed to add user to group: {e}")
    
    def remove_user_from_group(self, user_id, group_id):
        """
        Remove a user from a group
        
        Args:
            user_id (str): User ID
            group_id (str): Group ID
            
        Returns:
            dict: Operation status
            
        Raises:
            Exception: If the request fails
        """
        logger.info(f"Removing user {user_id} from group {group_id}")
        
        url = f"{self.api_url}/groups/{group_id}/users/{user_id}"
        
        try:
            response = requests.delete(
                url,
                headers=self.auth_service.get_headers()
            )
            response.raise_for_status()
            
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"Failed to remove user from group: {e}")
            raise Exception(f"Failed to remove user from group: {e}")
    
    def get_workspace_config(self):
        """
        Get workspace configuration
        
        Returns:
            dict: Workspace configuration
            
        Raises:
            Exception: If the request fails
        """
        logger.info("Getting workspace configuration")
        
        url = f"{self.api_url}/admin/config"
        
        try:
            response = requests.get(
                url,
                headers=self.auth_service.get_headers()
            )
            response.raise_for_status()
            
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"Failed to get workspace configuration: {e}")
            raise Exception(f"Failed to get workspace configuration: {e}")
    
    def update_workspace_config(self, config_data):
        """
        Update workspace configuration
        
        Args:
            config_data (dict): Updated configuration data
            
        Returns:
            dict: Updated workspace configuration
            
        Raises:
            Exception: If the request fails
        """
        logger.info("Updating workspace configuration")
        
        url = f"{self.api_url}/admin/config"
        
        try:
            response = requests.put(
                url,
                json=config_data,
                headers=self.auth_service.get_headers()
            )
            response.raise_for_status()
            
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"Failed to update workspace configuration: {e}")
            raise Exception(f"Failed to update workspace configuration: {e}")
    
    def get_audit_logs(self, start_time=None, end_time=None, user_id=None, action=None, limit=100, offset=0):
        """
        Get audit logs
        
        Args:
            start_time (int, optional): Start time in milliseconds since epoch
            end_time (int, optional): End time in milliseconds since epoch
            user_id (str, optional): Filter by user ID
            action (str, optional): Filter by action type
            limit (int): Maximum number of logs to return
            offset (int): Offset for pagination
            
        Returns:
            dict: Audit logs and pagination information
            
        Raises:
            Exception: If the request fails
        """
        logger.info(f"Getting audit logs (limit={limit}, offset={offset})")
        
        url = f"{self.api_url}/admin/audit"
        
        params = {
            'limit': limit,
            'offset': offset
        }
        
        if start_time:
            params['startTime'] = start_time
        
        if end_time:
            params['endTime'] = end_time
        
        if user_id:
            params['userId'] = user_id
        
        if action:
            params['action'] = action
        
        try:
            response = requests.get(
                url,
                params=params,
                headers=self.auth_service.get_headers()
            )
            response.raise_for_status()
            
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"Failed to get audit logs: {e}")
            raise Exception(f"Failed to get audit logs: {e}")
    
    def get_usage_metrics(self, start_time=None, end_time=None, metric_type=None):
        """
        Get usage metrics
        
        Args:
            start_time (int, optional): Start time in milliseconds since epoch
            end_time (int, optional): End time in milliseconds since epoch
            metric_type (str, optional): Type of metric to retrieve
            
        Returns:
            dict: Usage metrics
            
        Raises:
            Exception: If the request fails
        """
        logger.info("Getting usage metrics")
        
        url = f"{self.api_url}/admin/metrics"
        
        params = {}
        
        if start_time:
            params['startTime'] = start_time
        
        if end_time:
            params['endTime'] = end_time
        
        if metric_type:
            params['type'] = metric_type
        
        try:
            response = requests.get(
                url,
                params=params,
                headers=self.auth_service.get_headers()
            )
            response.raise_for_status()
            
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"Failed to get usage metrics: {e}")
            raise Exception(f"Failed to get usage metrics: {e}")
    
    def get_api_keys(self, limit=10, offset=0):
        """
        Get API keys
        
        Args:
            limit (int): Maximum number of API keys to return
            offset (int): Offset for pagination
            
        Returns:
            dict: API keys and pagination information
            
        Raises:
            Exception: If the request fails
        """
        logger.info(f"Getting API keys (limit={limit}, offset={offset})")
        
        url = f"{self.api_url}/admin/apikeys"
        
        params = {
            'limit': limit,
            'offset': offset
        }
        
        try:
            response = requests.get(
                url,
                params=params,
                headers=self.auth_service.get_headers()
            )
            response.raise_for_status()
            
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"Failed to get API keys: {e}")
            raise Exception(f"Failed to get API keys: {e}")
    
    def create_api_key(self, name, description=None, expiry=None):
        """
        Create a new API key
        
        Args:
            name (str): API key name
            description (str, optional): API key description
            expiry (int, optional): Expiry time in milliseconds since epoch
            
        Returns:
            dict: Created API key
            
        Raises:
            Exception: If the request fails
        """
        logger.info(f"Creating API key: {name}")
        
        url = f"{self.api_url}/admin/apikeys"
        
        payload = {
            'name': name
        }
        
        if description:
            payload['description'] = description
        
        if expiry:
            payload['expiry'] = expiry
        
        try:
            response = requests.post(
                url,
                json=payload,
                headers=self.auth_service.get_headers()
            )
            response.raise_for_status()
            
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"Failed to create API key: {e}")
            raise Exception(f"Failed to create API key: {e}")
    
    def delete_api_key(self, key_id):
        """
        Delete an API key
        
        Args:
            key_id (str): API key ID
            
        Returns:
            dict: Deletion status
            
        Raises:
            Exception: If the request fails
        """
        logger.info(f"Deleting API key with ID: {key_id}")
        
        url = f"{self.api_url}/admin/apikeys/{key_id}"
        
        try:
            response = requests.delete(
                url,
                headers=self.auth_service.get_headers()
            )
            response.raise_for_status()
            
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"Failed to delete API key: {e}")
            raise Exception(f"Failed to delete API key: {e}")
