"""
Search Service for Atlan Integration

This service handles interactions with Atlan's search APIs, including:
- Basic search
- Advanced search
- Faceted search
- Saved searches
"""

import logging
import requests
import json
from flask import current_app

logger = logging.getLogger(__name__)

class SearchService:
    """
    Service for handling Atlan search operations
    """
    
    def __init__(self, config, auth_service):
        """
        Initialize the search service
        
        Args:
            config: Application configuration
            auth_service: Authentication service
        """
        self.config = config
        self.auth_service = auth_service
        self.api_url = config.get('ATLAN_API_URL')
        
        logger.info("Search service initialized")
    
    def basic_search(self, query, limit=10, offset=0):
        """
        Perform a basic search
        
        Args:
            query (str): Search query
            limit (int): Maximum number of results to return
            offset (int): Offset for pagination
            
        Returns:
            dict: Search results and pagination information
            
        Raises:
            Exception: If the request fails
        """
        logger.info(f"Performing basic search: {query}")
        
        url = f"{self.api_url}/search"
        
        payload = {
            'query': query,
            'limit': limit,
            'offset': offset,
            'excludeDeletedEntities': True
        }
        
        try:
            response = requests.post(
                url,
                json=payload,
                headers=self.auth_service.get_headers()
            )
            response.raise_for_status()
            
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"Failed to perform basic search: {e}")
            raise Exception(f"Failed to perform basic search: {e}")
    
    def advanced_search(self, query, type_names=None, classification_names=None, term_guids=None, 
                       attribute_filters=None, sort_by=None, sort_order=None, limit=10, offset=0):
        """
        Perform an advanced search
        
        Args:
            query (str): Search query
            type_names (list, optional): List of entity type names to filter by
            classification_names (list, optional): List of classification names to filter by
            term_guids (list, optional): List of term GUIDs to filter by
            attribute_filters (dict, optional): Dictionary of attribute filters
            sort_by (str, optional): Field to sort by
            sort_order (str, optional): Sort order ('asc' or 'desc')
            limit (int): Maximum number of results to return
            offset (int): Offset for pagination
            
        Returns:
            dict: Search results and pagination information
            
        Raises:
            Exception: If the request fails
        """
        logger.info(f"Performing advanced search: {query}")
        
        url = f"{self.api_url}/search"
        
        payload = {
            'query': query,
            'limit': limit,
            'offset': offset,
            'excludeDeletedEntities': True
        }
        
        if type_names:
            payload['typeName'] = type_names
        
        if classification_names:
            payload['classification'] = classification_names
        
        if term_guids:
            payload['termGuid'] = term_guids
        
        if attribute_filters:
            payload['attributeFilters'] = attribute_filters
        
        if sort_by:
            payload['sortBy'] = sort_by
        
        if sort_order:
            payload['sortOrder'] = sort_order
        
        try:
            response = requests.post(
                url,
                json=payload,
                headers=self.auth_service.get_headers()
            )
            response.raise_for_status()
            
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"Failed to perform advanced search: {e}")
            raise Exception(f"Failed to perform advanced search: {e}")
    
    def faceted_search(self, query, facets, limit=10, offset=0):
        """
        Perform a faceted search
        
        Args:
            query (str): Search query
            facets (list): List of facets to include
            limit (int): Maximum number of results to return
            offset (int): Offset for pagination
            
        Returns:
            dict: Search results, facets, and pagination information
            
        Raises:
            Exception: If the request fails
        """
        logger.info(f"Performing faceted search: {query}")
        
        url = f"{self.api_url}/search/facets"
        
        payload = {
            'query': query,
            'limit': limit,
            'offset': offset,
            'excludeDeletedEntities': True,
            'facets': facets
        }
        
        try:
            response = requests.post(
                url,
                json=payload,
                headers=self.auth_service.get_headers()
            )
            response.raise_for_status()
            
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"Failed to perform faceted search: {e}")
            raise Exception(f"Failed to perform faceted search: {e}")
    
    def suggest(self, query, type_names=None, limit=10):
        """
        Get search suggestions
        
        Args:
            query (str): Search query
            type_names (list, optional): List of entity type names to filter by
            limit (int): Maximum number of suggestions to return
            
        Returns:
            dict: Search suggestions
            
        Raises:
            Exception: If the request fails
        """
        logger.info(f"Getting search suggestions: {query}")
        
        url = f"{self.api_url}/search/suggest"
        
        payload = {
            'query': query,
            'limit': limit
        }
        
        if type_names:
            payload['typeName'] = type_names
        
        try:
            response = requests.post(
                url,
                json=payload,
                headers=self.auth_service.get_headers()
            )
            response.raise_for_status()
            
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"Failed to get search suggestions: {e}")
            raise Exception(f"Failed to get search suggestions: {e}")
    
    def get_saved_searches(self, limit=10, offset=0):
        """
        Get saved searches
        
        Args:
            limit (int): Maximum number of saved searches to return
            offset (int): Offset for pagination
            
        Returns:
            dict: Saved searches and pagination information
            
        Raises:
            Exception: If the request fails
        """
        logger.info(f"Getting saved searches (limit={limit}, offset={offset})")
        
        url = f"{self.api_url}/search/saved"
        
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
            logger.error(f"Failed to get saved searches: {e}")
            raise Exception(f"Failed to get saved searches: {e}")
    
    def get_saved_search(self, guid):
        """
        Get a saved search by GUID
        
        Args:
            guid (str): Saved search GUID
            
        Returns:
            dict: Saved search details
            
        Raises:
            Exception: If the request fails
        """
        logger.info(f"Getting saved search with GUID: {guid}")
        
        url = f"{self.api_url}/search/saved/{guid}"
        
        try:
            response = requests.get(
                url,
                headers=self.auth_service.get_headers()
            )
            response.raise_for_status()
            
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"Failed to get saved search: {e}")
            raise Exception(f"Failed to get saved search: {e}")
    
    def create_saved_search(self, name, query, type_names=None, classification_names=None, 
                           term_guids=None, attribute_filters=None, sort_by=None, sort_order=None):
        """
        Create a saved search
        
        Args:
            name (str): Saved search name
            query (str): Search query
            type_names (list, optional): List of entity type names to filter by
            classification_names (list, optional): List of classification names to filter by
            term_guids (list, optional): List of term GUIDs to filter by
            attribute_filters (dict, optional): Dictionary of attribute filters
            sort_by (str, optional): Field to sort by
            sort_order (str, optional): Sort order ('asc' or 'desc')
            
        Returns:
            dict: Created saved search
            
        Raises:
            Exception: If the request fails
        """
        logger.info(f"Creating saved search: {name}")
        
        url = f"{self.api_url}/search/saved"
        
        payload = {
            'name': name,
            'query': query,
            'excludeDeletedEntities': True
        }
        
        if type_names:
            payload['typeName'] = type_names
        
        if classification_names:
            payload['classification'] = classification_names
        
        if term_guids:
            payload['termGuid'] = term_guids
        
        if attribute_filters:
            payload['attributeFilters'] = attribute_filters
        
        if sort_by:
            payload['sortBy'] = sort_by
        
        if sort_order:
            payload['sortOrder'] = sort_order
        
        try:
            response = requests.post(
                url,
                json=payload,
                headers=self.auth_service.get_headers()
            )
            response.raise_for_status()
            
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"Failed to create saved search: {e}")
            raise Exception(f"Failed to create saved search: {e}")
    
    def update_saved_search(self, guid, saved_search_data):
        """
        Update a saved search
        
        Args:
            guid (str): Saved search GUID
            saved_search_data (dict): Updated saved search data
            
        Returns:
            dict: Updated saved search
            
        Raises:
            Exception: If the request fails
        """
        logger.info(f"Updating saved search with GUID: {guid}")
        
        url = f"{self.api_url}/search/saved/{guid}"
        
        try:
            response = requests.put(
                url,
                json=saved_search_data,
                headers=self.auth_service.get_headers()
            )
            response.raise_for_status()
            
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"Failed to update saved search: {e}")
            raise Exception(f"Failed to update saved search: {e}")
    
    def delete_saved_search(self, guid):
        """
        Delete a saved search
        
        Args:
            guid (str): Saved search GUID
            
        Returns:
            dict: Deletion status
            
        Raises:
            Exception: If the request fails
        """
        logger.info(f"Deleting saved search with GUID: {guid}")
        
        url = f"{self.api_url}/search/saved/{guid}"
        
        try:
            response = requests.delete(
                url,
                headers=self.auth_service.get_headers()
            )
            response.raise_for_status()
            
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"Failed to delete saved search: {e}")
            raise Exception(f"Failed to delete saved search: {e}")
    
    def execute_saved_search(self, guid, limit=10, offset=0):
        """
        Execute a saved search
        
        Args:
            guid (str): Saved search GUID
            limit (int): Maximum number of results to return
            offset (int): Offset for pagination
            
        Returns:
            dict: Search results and pagination information
            
        Raises:
            Exception: If the request fails
        """
        logger.info(f"Executing saved search with GUID: {guid}")
        
        url = f"{self.api_url}/search/saved/{guid}/execute"
        
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
            logger.error(f"Failed to execute saved search: {e}")
            raise Exception(f"Failed to execute saved search: {e}")
