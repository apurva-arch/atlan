"""
Asset Service for Atlan Integration

This service handles interactions with Atlan's asset APIs, including:
- Asset creation, retrieval, update, and deletion
- Asset classification and tagging
- Asset relationships
- Custom attributes
"""

import logging
import requests
import json
from flask import current_app

logger = logging.getLogger(__name__)

class AssetService:
    """
    Service for handling Atlan asset operations
    """
    
    def __init__(self, config, auth_service):
        """
        Initialize the asset service
        
        Args:
            config: Application configuration
            auth_service: Authentication service
        """
        self.config = config
        self.auth_service = auth_service
        self.api_url = config.get('ATLAN_API_URL')
        
        logger.info("Asset service initialized")
    
    def get_assets(self, limit=10, offset=0, sort_by=None, order=None, filter_expr=None):
        """
        Get a list of assets
        
        Args:
            limit (int): Maximum number of assets to return
            offset (int): Offset for pagination
            sort_by (str): Field to sort by
            order (str): Sort order ('asc' or 'desc')
            filter_expr (str): Filter expression
            
        Returns:
            dict: List of assets and pagination information
            
        Raises:
            Exception: If the request fails
        """
        logger.info(f"Getting assets (limit={limit}, offset={offset})")
        
        url = f"{self.api_url}/assets"
        
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
            logger.error(f"Failed to get assets: {e}")
            raise Exception(f"Failed to get assets: {e}")
    
    def get_asset(self, guid):
        """
        Get an asset by GUID
        
        Args:
            guid (str): Asset GUID
            
        Returns:
            dict: Asset details
            
        Raises:
            Exception: If the request fails
        """
        logger.info(f"Getting asset with GUID: {guid}")
        
        url = f"{self.api_url}/assets/{guid}"
        
        try:
            response = requests.get(
                url,
                headers=self.auth_service.get_headers()
            )
            response.raise_for_status()
            
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"Failed to get asset: {e}")
            raise Exception(f"Failed to get asset: {e}")
    
    def create_asset(self, asset_data):
        """
        Create a new asset
        
        Args:
            asset_data (dict): Asset data
            
        Returns:
            dict: Created asset
            
        Raises:
            Exception: If the request fails
        """
        logger.info(f"Creating asset: {asset_data.get('typeName')}")
        
        url = f"{self.api_url}/assets"
        
        try:
            response = requests.post(
                url,
                json=asset_data,
                headers=self.auth_service.get_headers()
            )
            response.raise_for_status()
            
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"Failed to create asset: {e}")
            raise Exception(f"Failed to create asset: {e}")
    
    def update_asset(self, guid, asset_data):
        """
        Update an asset
        
        Args:
            guid (str): Asset GUID
            asset_data (dict): Updated asset data
            
        Returns:
            dict: Updated asset
            
        Raises:
            Exception: If the request fails
        """
        logger.info(f"Updating asset with GUID: {guid}")
        
        url = f"{self.api_url}/assets/{guid}"
        
        try:
            response = requests.put(
                url,
                json=asset_data,
                headers=self.auth_service.get_headers()
            )
            response.raise_for_status()
            
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"Failed to update asset: {e}")
            raise Exception(f"Failed to update asset: {e}")
    
    def delete_asset(self, guid):
        """
        Delete an asset
        
        Args:
            guid (str): Asset GUID
            
        Returns:
            dict: Deletion status
            
        Raises:
            Exception: If the request fails
        """
        logger.info(f"Deleting asset with GUID: {guid}")
        
        url = f"{self.api_url}/assets/{guid}"
        
        try:
            response = requests.delete(
                url,
                headers=self.auth_service.get_headers()
            )
            response.raise_for_status()
            
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"Failed to delete asset: {e}")
            raise Exception(f"Failed to delete asset: {e}")
    
    def add_classification(self, guid, classification):
        """
        Add a classification to an asset
        
        Args:
            guid (str): Asset GUID
            classification (dict): Classification data
            
        Returns:
            dict: Updated asset
            
        Raises:
            Exception: If the request fails
        """
        logger.info(f"Adding classification to asset with GUID: {guid}")
        
        url = f"{self.api_url}/assets/{guid}/classifications"
        
        try:
            response = requests.post(
                url,
                json=classification,
                headers=self.auth_service.get_headers()
            )
            response.raise_for_status()
            
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"Failed to add classification: {e}")
            raise Exception(f"Failed to add classification: {e}")
    
    def remove_classification(self, guid, classification_name):
        """
        Remove a classification from an asset
        
        Args:
            guid (str): Asset GUID
            classification_name (str): Classification name
            
        Returns:
            dict: Updated asset
            
        Raises:
            Exception: If the request fails
        """
        logger.info(f"Removing classification from asset with GUID: {guid}")
        
        url = f"{self.api_url}/assets/{guid}/classifications/{classification_name}"
        
        try:
            response = requests.delete(
                url,
                headers=self.auth_service.get_headers()
            )
            response.raise_for_status()
            
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"Failed to remove classification: {e}")
            raise Exception(f"Failed to remove classification: {e}")
    
    def add_term(self, guid, term_guid):
        """
        Add a term to an asset
        
        Args:
            guid (str): Asset GUID
            term_guid (str): Term GUID
            
        Returns:
            dict: Updated asset
            
        Raises:
            Exception: If the request fails
        """
        logger.info(f"Adding term to asset with GUID: {guid}")
        
        url = f"{self.api_url}/assets/{guid}/terms"
        
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
            logger.error(f"Failed to add term: {e}")
            raise Exception(f"Failed to add term: {e}")
    
    def remove_term(self, guid, term_guid):
        """
        Remove a term from an asset
        
        Args:
            guid (str): Asset GUID
            term_guid (str): Term GUID
            
        Returns:
            dict: Updated asset
            
        Raises:
            Exception: If the request fails
        """
        logger.info(f"Removing term from asset with GUID: {guid}")
        
        url = f"{self.api_url}/assets/{guid}/terms/{term_guid}"
        
        try:
            response = requests.delete(
                url,
                headers=self.auth_service.get_headers()
            )
            response.raise_for_status()
            
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"Failed to remove term: {e}")
            raise Exception(f"Failed to remove term: {e}")
    
    def get_asset_schema(self, type_name):
        """
        Get the schema for an asset type
        
        Args:
            type_name (str): Asset type name
            
        Returns:
            dict: Asset schema
            
        Raises:
            Exception: If the request fails
        """
        logger.info(f"Getting schema for asset type: {type_name}")
        
        url = f"{self.api_url}/types/entityDefs/{type_name}"
        
        try:
            response = requests.get(
                url,
                headers=self.auth_service.get_headers()
            )
            response.raise_for_status()
            
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"Failed to get asset schema: {e}")
            raise Exception(f"Failed to get asset schema: {e}")
    
    def get_asset_types(self):
        """
        Get all asset types
        
        Returns:
            list: List of asset types
            
        Raises:
            Exception: If the request fails
        """
        logger.info("Getting all asset types")
        
        url = f"{self.api_url}/types/entityDefs"
        
        try:
            response = requests.get(
                url,
                headers=self.auth_service.get_headers()
            )
            response.raise_for_status()
            
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"Failed to get asset types: {e}")
            raise Exception(f"Failed to get asset types: {e}")
    
    def get_asset_relationships(self, guid, relationship_type=None):
        """
        Get relationships for an asset
        
        Args:
            guid (str): Asset GUID
            relationship_type (str, optional): Relationship type
            
        Returns:
            dict: Asset relationships
            
        Raises:
            Exception: If the request fails
        """
        logger.info(f"Getting relationships for asset with GUID: {guid}")
        
        url = f"{self.api_url}/assets/{guid}/relationships"
        
        params = {}
        if relationship_type:
            params['relationshipType'] = relationship_type
        
        try:
            response = requests.get(
                url,
                params=params,
                headers=self.auth_service.get_headers()
            )
            response.raise_for_status()
            
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"Failed to get asset relationships: {e}")
            raise Exception(f"Failed to get asset relationships: {e}")
    
    def create_relationship(self, from_guid, to_guid, relationship_type):
        """
        Create a relationship between two assets
        
        Args:
            from_guid (str): Source asset GUID
            to_guid (str): Target asset GUID
            relationship_type (str): Relationship type
            
        Returns:
            dict: Created relationship
            
        Raises:
            Exception: If the request fails
        """
        logger.info(f"Creating relationship between assets: {from_guid} -> {to_guid}")
        
        url = f"{self.api_url}/relationships"
        
        payload = {
            'fromEntityGuid': from_guid,
            'toEntityGuid': to_guid,
            'relationshipType': relationship_type
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
            logger.error(f"Failed to create relationship: {e}")
            raise Exception(f"Failed to create relationship: {e}")
