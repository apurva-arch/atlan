"""
Glossary Service for Atlan Integration

This service handles interactions with Atlan's glossary APIs, including:
- Term management
- Category management
- Term assignments
- Glossary hierarchies
"""

import logging
import requests
import json
from flask import current_app

logger = logging.getLogger(__name__)

class GlossaryService:
    """
    Service for handling Atlan glossary operations
    """
    
    def __init__(self, config, auth_service):
        """
        Initialize the glossary service
        
        Args:
            config: Application configuration
            auth_service: Authentication service
        """
        self.config = config
        self.auth_service = auth_service
        self.api_url = config.get('ATLAN_API_URL')
        
        logger.info("Glossary service initialized")
    
    def get_glossaries(self, limit=10, offset=0):
        """
        Get a list of glossaries
        
        Args:
            limit (int): Maximum number of glossaries to return
            offset (int): Offset for pagination
            
        Returns:
            dict: List of glossaries and pagination information
            
        Raises:
            Exception: If the request fails
        """
        logger.info(f"Getting glossaries (limit={limit}, offset={offset})")
        
        url = f"{self.api_url}/glossary"
        
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
            logger.error(f"Failed to get glossaries: {e}")
            raise Exception(f"Failed to get glossaries: {e}")
    
    def get_glossary(self, guid):
        """
        Get a glossary by GUID
        
        Args:
            guid (str): Glossary GUID
            
        Returns:
            dict: Glossary details
            
        Raises:
            Exception: If the request fails
        """
        logger.info(f"Getting glossary with GUID: {guid}")
        
        url = f"{self.api_url}/glossary/{guid}"
        
        try:
            response = requests.get(
                url,
                headers=self.auth_service.get_headers()
            )
            response.raise_for_status()
            
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"Failed to get glossary: {e}")
            raise Exception(f"Failed to get glossary: {e}")
    
    def create_glossary(self, glossary_data):
        """
        Create a new glossary
        
        Args:
            glossary_data (dict): Glossary data
            
        Returns:
            dict: Created glossary
            
        Raises:
            Exception: If the request fails
        """
        logger.info(f"Creating glossary: {glossary_data.get('name')}")
        
        url = f"{self.api_url}/glossary"
        
        try:
            response = requests.post(
                url,
                json=glossary_data,
                headers=self.auth_service.get_headers()
            )
            response.raise_for_status()
            
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"Failed to create glossary: {e}")
            raise Exception(f"Failed to create glossary: {e}")
    
    def update_glossary(self, guid, glossary_data):
        """
        Update a glossary
        
        Args:
            guid (str): Glossary GUID
            glossary_data (dict): Updated glossary data
            
        Returns:
            dict: Updated glossary
            
        Raises:
            Exception: If the request fails
        """
        logger.info(f"Updating glossary with GUID: {guid}")
        
        url = f"{self.api_url}/glossary/{guid}"
        
        try:
            response = requests.put(
                url,
                json=glossary_data,
                headers=self.auth_service.get_headers()
            )
            response.raise_for_status()
            
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"Failed to update glossary: {e}")
            raise Exception(f"Failed to update glossary: {e}")
    
    def delete_glossary(self, guid):
        """
        Delete a glossary
        
        Args:
            guid (str): Glossary GUID
            
        Returns:
            dict: Deletion status
            
        Raises:
            Exception: If the request fails
        """
        logger.info(f"Deleting glossary with GUID: {guid}")
        
        url = f"{self.api_url}/glossary/{guid}"
        
        try:
            response = requests.delete(
                url,
                headers=self.auth_service.get_headers()
            )
            response.raise_for_status()
            
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"Failed to delete glossary: {e}")
            raise Exception(f"Failed to delete glossary: {e}")
    
    def get_terms(self, glossary_guid=None, category_guid=None, limit=10, offset=0, sort_by=None, order=None, filter_expr=None):
        """
        Get a list of terms
        
        Args:
            glossary_guid (str, optional): Glossary GUID
            category_guid (str, optional): Category GUID
            limit (int): Maximum number of terms to return
            offset (int): Offset for pagination
            sort_by (str): Field to sort by
            order (str): Sort order ('asc' or 'desc')
            filter_expr (str): Filter expression
            
        Returns:
            dict: List of terms and pagination information
            
        Raises:
            Exception: If the request fails
        """
        logger.info(f"Getting terms (limit={limit}, offset={offset})")
        
        url = f"{self.api_url}/glossary/terms"
        
        params = {
            'limit': limit,
            'offset': offset
        }
        
        if glossary_guid:
            params['glossaryGuid'] = glossary_guid
        
        if category_guid:
            params['categoryGuid'] = category_guid
        
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
            logger.error(f"Failed to get terms: {e}")
            raise Exception(f"Failed to get terms: {e}")
    
    def get_term(self, guid):
        """
        Get a term by GUID
        
        Args:
            guid (str): Term GUID
            
        Returns:
            dict: Term details
            
        Raises:
            Exception: If the request fails
        """
        logger.info(f"Getting term with GUID: {guid}")
        
        url = f"{self.api_url}/glossary/terms/{guid}"
        
        try:
            response = requests.get(
                url,
                headers=self.auth_service.get_headers()
            )
            response.raise_for_status()
            
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"Failed to get term: {e}")
            raise Exception(f"Failed to get term: {e}")
    
    def create_term(self, term_data):
        """
        Create a new term
        
        Args:
            term_data (dict): Term data
            
        Returns:
            dict: Created term
            
        Raises:
            Exception: If the request fails
        """
        logger.info(f"Creating term: {term_data.get('name')}")
        
        url = f"{self.api_url}/glossary/terms"
        
        try:
            response = requests.post(
                url,
                json=term_data,
                headers=self.auth_service.get_headers()
            )
            response.raise_for_status()
            
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"Failed to create term: {e}")
            raise Exception(f"Failed to create term: {e}")
    
    def update_term(self, guid, term_data):
        """
        Update a term
        
        Args:
            guid (str): Term GUID
            term_data (dict): Updated term data
            
        Returns:
            dict: Updated term
            
        Raises:
            Exception: If the request fails
        """
        logger.info(f"Updating term with GUID: {guid}")
        
        url = f"{self.api_url}/glossary/terms/{guid}"
        
        try:
            response = requests.put(
                url,
                json=term_data,
                headers=self.auth_service.get_headers()
            )
            response.raise_for_status()
            
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"Failed to update term: {e}")
            raise Exception(f"Failed to update term: {e}")
    
    def delete_term(self, guid):
        """
        Delete a term
        
        Args:
            guid (str): Term GUID
            
        Returns:
            dict: Deletion status
            
        Raises:
            Exception: If the request fails
        """
        logger.info(f"Deleting term with GUID: {guid}")
        
        url = f"{self.api_url}/glossary/terms/{guid}"
        
        try:
            response = requests.delete(
                url,
                headers=self.auth_service.get_headers()
            )
            response.raise_for_status()
            
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"Failed to delete term: {e}")
            raise Exception(f"Failed to delete term: {e}")
    
    def get_categories(self, glossary_guid=None, parent_category_guid=None, limit=10, offset=0):
        """
        Get a list of categories
        
        Args:
            glossary_guid (str, optional): Glossary GUID
            parent_category_guid (str, optional): Parent category GUID
            limit (int): Maximum number of categories to return
            offset (int): Offset for pagination
            
        Returns:
            dict: List of categories and pagination information
            
        Raises:
            Exception: If the request fails
        """
        logger.info(f"Getting categories (limit={limit}, offset={offset})")
        
        url = f"{self.api_url}/glossary/categories"
        
        params = {
            'limit': limit,
            'offset': offset
        }
        
        if glossary_guid:
            params['glossaryGuid'] = glossary_guid
        
        if parent_category_guid:
            params['parentCategoryGuid'] = parent_category_guid
        
        try:
            response = requests.get(
                url,
                params=params,
                headers=self.auth_service.get_headers()
            )
            response.raise_for_status()
            
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"Failed to get categories: {e}")
            raise Exception(f"Failed to get categories: {e}")
    
    def get_category(self, guid):
        """
        Get a category by GUID
        
        Args:
            guid (str): Category GUID
            
        Returns:
            dict: Category details
            
        Raises:
            Exception: If the request fails
        """
        logger.info(f"Getting category with GUID: {guid}")
        
        url = f"{self.api_url}/glossary/categories/{guid}"
        
        try:
            response = requests.get(
                url,
                headers=self.auth_service.get_headers()
            )
            response.raise_for_status()
            
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"Failed to get category: {e}")
            raise Exception(f"Failed to get category: {e}")
    
    def create_category(self, category_data):
        """
        Create a new category
        
        Args:
            category_data (dict): Category data
            
        Returns:
            dict: Created category
            
        Raises:
            Exception: If the request fails
        """
        logger.info(f"Creating category: {category_data.get('name')}")
        
        url = f"{self.api_url}/glossary/categories"
        
        try:
            response = requests.post(
                url,
                json=category_data,
                headers=self.auth_service.get_headers()
            )
            response.raise_for_status()
            
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"Failed to create category: {e}")
            raise Exception(f"Failed to create category: {e}")
    
    def update_category(self, guid, category_data):
        """
        Update a category
        
        Args:
            guid (str): Category GUID
            category_data (dict): Updated category data
            
        Returns:
            dict: Updated category
            
        Raises:
            Exception: If the request fails
        """
        logger.info(f"Updating category with GUID: {guid}")
        
        url = f"{self.api_url}/glossary/categories/{guid}"
        
        try:
            response = requests.put(
                url,
                json=category_data,
                headers=self.auth_service.get_headers()
            )
            response.raise_for_status()
            
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"Failed to update category: {e}")
            raise Exception(f"Failed to update category: {e}")
    
    def delete_category(self, guid):
        """
        Delete a category
        
        Args:
            guid (str): Category GUID
            
        Returns:
            dict: Deletion status
            
        Raises:
            Exception: If the request fails
        """
        logger.info(f"Deleting category with GUID: {guid}")
        
        url = f"{self.api_url}/glossary/categories/{guid}"
        
        try:
            response = requests.delete(
                url,
                headers=self.auth_service.get_headers()
            )
            response.raise_for_status()
            
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"Failed to delete category: {e}")
            raise Exception(f"Failed to delete category: {e}")
    
    def assign_term_to_asset(self, term_guid, asset_guid):
        """
        Assign a term to an asset
        
        Args:
            term_guid (str): Term GUID
            asset_guid (str): Asset GUID
            
        Returns:
            dict: Assignment status
            
        Raises:
            Exception: If the request fails
        """
        logger.info(f"Assigning term {term_guid} to asset {asset_guid}")
        
        url = f"{self.api_url}/assets/{asset_guid}/terms"
        
        payload = {
            'termGuid': term_guid
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
            logger.error(f"Failed to assign term to asset: {e}")
            raise Exception(f"Failed to assign term to asset: {e}")
    
    def remove_term_from_asset(self, term_guid, asset_guid):
        """
        Remove a term from an asset
        
        Args:
            term_guid (str): Term GUID
            asset_guid (str): Asset GUID
            
        Returns:
            dict: Removal status
            
        Raises:
            Exception: If the request fails
        """
        logger.info(f"Removing term {term_guid} from asset {asset_guid}")
        
        url = f"{self.api_url}/assets/{asset_guid}/terms/{term_guid}"
        
        try:
            response = requests.delete(
                url,
                headers=self.auth_service.get_headers()
            )
            response.raise_for_status()
            
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"Failed to remove term from asset: {e}")
            raise Exception(f"Failed to remove term from asset: {e}")
    
    def get_assets_with_term(self, term_guid, limit=10, offset=0):
        """
        Get assets assigned to a term
        
        Args:
            term_guid (str): Term GUID
            limit (int): Maximum number of assets to return
            offset (int): Offset for pagination
            
        Returns:
            dict: List of assets and pagination information
            
        Raises:
            Exception: If the request fails
        """
        logger.info(f"Getting assets with term {term_guid}")
        
        url = f"{self.api_url}/glossary/terms/{term_guid}/assets"
        
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
            logger.error(f"Failed to get assets with term: {e}")
            raise Exception(f"Failed to get assets with term: {e}")
