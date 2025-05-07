"""
Lineage Service for Atlan Integration

This service handles interactions with Atlan's lineage APIs, including:
- Lineage retrieval
- Lineage creation
- Impact analysis
- Process tracking
"""

import logging
import requests
import json
from flask import current_app

logger = logging.getLogger(__name__)

class LineageService:
    """
    Service for handling Atlan lineage operations
    """
    
    def __init__(self, config, auth_service):
        """
        Initialize the lineage service
        
        Args:
            config: Application configuration
            auth_service: Authentication service
        """
        self.config = config
        self.auth_service = auth_service
        self.api_url = config.get('ATLAN_API_URL')
        
        logger.info("Lineage service initialized")
    
    def get_lineage(self, guid, direction='BOTH', depth=3, include_process=True):
        """
        Get lineage for an asset
        
        Args:
            guid (str): Asset GUID
            direction (str): Lineage direction ('BOTH', 'INPUT', or 'OUTPUT')
            depth (int): Lineage depth
            include_process (bool): Whether to include process entities
            
        Returns:
            dict: Lineage information
            
        Raises:
            Exception: If the request fails
        """
        logger.info(f"Getting lineage for asset with GUID: {guid}")
        
        url = f"{self.api_url}/lineage"
        
        params = {
            'guid': guid,
            'direction': direction,
            'depth': depth,
            'includeProcess': include_process
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
            logger.error(f"Failed to get lineage: {e}")
            raise Exception(f"Failed to get lineage: {e}")
    
    def create_lineage(self, from_guid, to_guid, process_guid=None, process_name=None, process_type=None):
        """
        Create lineage between two assets
        
        Args:
            from_guid (str): Source asset GUID
            to_guid (str): Target asset GUID
            process_guid (str, optional): Process GUID
            process_name (str, optional): Process name
            process_type (str, optional): Process type
            
        Returns:
            dict: Created lineage
            
        Raises:
            Exception: If the request fails
        """
        logger.info(f"Creating lineage between assets: {from_guid} -> {to_guid}")
        
        url = f"{self.api_url}/lineage"
        
        # If process_guid is provided, use it
        if process_guid:
            payload = {
                'fromEntityGuid': from_guid,
                'toEntityGuid': to_guid,
                'processGuid': process_guid
            }
        # Otherwise, create a new process entity
        elif process_name and process_type:
            payload = {
                'fromEntityGuid': from_guid,
                'toEntityGuid': to_guid,
                'process': {
                    'typeName': process_type,
                    'attributes': {
                        'name': process_name,
                        'qualifiedName': f"{process_name}_{from_guid}_{to_guid}"
                    }
                }
            }
        # If neither is provided, create direct lineage
        else:
            payload = {
                'fromEntityGuid': from_guid,
                'toEntityGuid': to_guid
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
            logger.error(f"Failed to create lineage: {e}")
            raise Exception(f"Failed to create lineage: {e}")
    
    def delete_lineage(self, from_guid, to_guid, process_guid=None):
        """
        Delete lineage between two assets
        
        Args:
            from_guid (str): Source asset GUID
            to_guid (str): Target asset GUID
            process_guid (str, optional): Process GUID
            
        Returns:
            dict: Deletion status
            
        Raises:
            Exception: If the request fails
        """
        logger.info(f"Deleting lineage between assets: {from_guid} -> {to_guid}")
        
        url = f"{self.api_url}/lineage"
        
        params = {
            'fromEntityGuid': from_guid,
            'toEntityGuid': to_guid
        }
        
        if process_guid:
            params['processGuid'] = process_guid
        
        try:
            response = requests.delete(
                url,
                params=params,
                headers=self.auth_service.get_headers()
            )
            response.raise_for_status()
            
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"Failed to delete lineage: {e}")
            raise Exception(f"Failed to delete lineage: {e}")
    
    def get_impact_analysis(self, guid, depth=3):
        """
        Get impact analysis for an asset
        
        Args:
            guid (str): Asset GUID
            depth (int): Analysis depth
            
        Returns:
            dict: Impact analysis information
            
        Raises:
            Exception: If the request fails
        """
        logger.info(f"Getting impact analysis for asset with GUID: {guid}")
        
        url = f"{self.api_url}/lineage/impact"
        
        params = {
            'guid': guid,
            'depth': depth
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
            logger.error(f"Failed to get impact analysis: {e}")
            raise Exception(f"Failed to get impact analysis: {e}")
    
    def get_process_details(self, process_guid):
        """
        Get details for a process entity
        
        Args:
            process_guid (str): Process GUID
            
        Returns:
            dict: Process details
            
        Raises:
            Exception: If the request fails
        """
        logger.info(f"Getting details for process with GUID: {process_guid}")
        
        url = f"{self.api_url}/assets/{process_guid}"
        
        try:
            response = requests.get(
                url,
                headers=self.auth_service.get_headers()
            )
            response.raise_for_status()
            
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"Failed to get process details: {e}")
            raise Exception(f"Failed to get process details: {e}")
    
    def update_process(self, process_guid, process_data):
        """
        Update a process entity
        
        Args:
            process_guid (str): Process GUID
            process_data (dict): Updated process data
            
        Returns:
            dict: Updated process
            
        Raises:
            Exception: If the request fails
        """
        logger.info(f"Updating process with GUID: {process_guid}")
        
        url = f"{self.api_url}/assets/{process_guid}"
        
        try:
            response = requests.put(
                url,
                json=process_data,
                headers=self.auth_service.get_headers()
            )
            response.raise_for_status()
            
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"Failed to update process: {e}")
            raise Exception(f"Failed to update process: {e}")
    
    def get_lineage_graph(self, guid, direction='BOTH', depth=3, include_process=True):
        """
        Get lineage graph for visualization
        
        Args:
            guid (str): Asset GUID
            direction (str): Lineage direction ('BOTH', 'INPUT', or 'OUTPUT')
            depth (int): Lineage depth
            include_process (bool): Whether to include process entities
            
        Returns:
            dict: Lineage graph with nodes and edges
            
        Raises:
            Exception: If the request fails
        """
        logger.info(f"Getting lineage graph for asset with GUID: {guid}")
        
        # Get raw lineage data
        lineage_data = self.get_lineage(guid, direction, depth, include_process)
        
        # Transform into graph format
        graph = {
            'nodes': [],
            'edges': []
        }
        
        # Process nodes
        if 'entities' in lineage_data:
            for entity in lineage_data['entities']:
                node = {
                    'id': entity['guid'],
                    'label': entity['attributes'].get('name', 'Unknown'),
                    'type': entity['typeName'],
                    'data': entity
                }
                graph['nodes'].append(node)
        
        # Process edges
        if 'relations' in lineage_data:
            for relation in lineage_data['relations']:
                edge = {
                    'id': f"{relation['fromEntityGuid']}_{relation['toEntityGuid']}",
                    'source': relation['fromEntityGuid'],
                    'target': relation['toEntityGuid'],
                    'label': relation.get('relationshipType', 'Unknown'),
                    'data': relation
                }
                graph['edges'].append(edge)
        
        return graph
