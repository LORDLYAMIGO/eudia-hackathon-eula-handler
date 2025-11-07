import os
import re
from pathlib import Path
from typing import Optional, Dict, List
from urllib.parse import urlparse


class EULAService:
    def __init__(self, eula_base_path: str):
        self.eula_base_path = Path(eula_base_path)
    
    def extract_domain(self, url: str) -> Optional[str]:
        """
        Extract domain from various URL formats.
        Supports:
        - https://google.com
        - http://www.google.com
        - google.com
        - www.google.com
        - chatgpt.com
        """
        # Remove whitespace
        url = url.strip()
        
        # If it doesn't start with http/https, add it for parsing
        if not url.startswith(('http://', 'https://')):
            url = 'https://' + url
        
        # Parse the URL
        parsed = urlparse(url)
        domain = parsed.netloc or parsed.path
        
        # Remove www. prefix if present
        if domain.startswith('www.'):
            domain = domain[4:]
        
        # Remove any trailing slashes or paths
        domain = domain.split('/')[0]
        
        return domain if domain else None
    
    def find_domain_folder(self, domain: str) -> Optional[Path]:
        """
        Find the matching domain folder in EULA directory.
        Handles case-insensitive matching and various folder naming conventions.
        """
        if not domain:
            return None
        
        # List all folders in EULA directory
        for folder in self.eula_base_path.iterdir():
            if folder.is_dir():
                folder_name = folder.name.lower()
                domain_lower = domain.lower()
                
                # Direct match
                if folder_name == domain_lower:
                    return folder
                
                # Check if domain is part of folder name (for cases like google.com_maps)
                if folder_name.startswith(domain_lower):
                    return folder
        
        return None
    
    def get_markdown_files_sorted(self, folder_path: Path) -> List[Path]:
        """
        Get all markdown files in a folder, sorted by date (oldest to newest).
        The date is extracted from the filename format: YYYY-MM-DDTHH-MM-SSZ.md
        """
        if not folder_path.exists():
            return []
        
        md_files = list(folder_path.glob("*.md"))
        # Sort by filename (which is the ISO date format)
        md_files.sort()
        return md_files
    
    def read_markdown_file(self, file_path: Path) -> str:
        """Read and return the content of a markdown file."""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                return f.read()
        except Exception as e:
            return f"Error reading file: {str(e)}"
    
    def get_latest_eula(self, domain: str, doc_type: Optional[str] = None) -> Dict[str, any]:
        """
        Get the latest EULA document for a domain.
        
        Args:
            domain: The domain name (e.g., 'chatgpt.com', 'https://google.com')
            doc_type: Optional document type ('Privacy Policy' or 'Terms of Service')
        
        Returns:
            Dict with 'EULA' key containing the markdown content, or error message
        """
        # Extract and find domain
        clean_domain = self.extract_domain(domain)
        domain_folder = self.find_domain_folder(clean_domain)
        
        if not domain_folder:
            return {
                "error": f"Domain '{domain}' not found in EULA database",
                "domain_extracted": clean_domain
            }
        
        # Look for document type folders
        doc_types = []
        if doc_type:
            doc_types = [doc_type]
        else:
            # Check both if not specified
            for dt in ["Privacy Policy", "Terms of Service"]:
                dt_path = domain_folder / dt
                if dt_path.exists() and dt_path.is_dir():
                    doc_types.append(dt)
        
        if not doc_types:
            return {
                "error": f"No Privacy Policy or Terms of Service found for domain '{clean_domain}'",
                "domain_folder": str(domain_folder)
            }
        
        # Get the latest file from the first available doc type
        target_folder = domain_folder / doc_types[0]
        md_files = self.get_markdown_files_sorted(target_folder)
        
        if not md_files:
            return {
                "error": f"No markdown files found in {doc_types[0]}",
                "domain_folder": str(domain_folder)
            }
        
        # Get the latest (last in sorted list)
        latest_file = md_files[-1]
        content = self.read_markdown_file(latest_file)
        
        return {
            "EULA": content,
            "metadata": {
                "domain": clean_domain,
                "document_type": doc_types[0],
                "file_name": latest_file.name,
                "file_date": latest_file.stem,  # Date part of filename
                "total_versions": len(md_files)
            }
        }
    
    def get_archive_eula(self, domain: str, doc_type: Optional[str] = None) -> Dict[str, any]:
        """
        Get all archived EULA documents for a domain, chained together.
        
        Args:
            domain: The domain name (e.g., 'chatgpt.com', 'https://google.com')
            doc_type: Optional document type ('Privacy Policy' or 'Terms of Service')
        
        Returns:
            Dict with 'EULA' key containing all markdown contents chained together
        """
        # Extract and find domain
        clean_domain = self.extract_domain(domain)
        domain_folder = self.find_domain_folder(clean_domain)
        
        if not domain_folder:
            return {
                "error": f"Domain '{domain}' not found in EULA database",
                "domain_extracted": clean_domain
            }
        
        # Look for document type folders
        doc_types = []
        if doc_type:
            doc_types = [doc_type]
        else:
            # Check both if not specified
            for dt in ["Privacy Policy", "Terms of Service"]:
                dt_path = domain_folder / dt
                if dt_path.exists() and dt_path.is_dir():
                    doc_types.append(dt)
        
        if not doc_types:
            return {
                "error": f"No Privacy Policy or Terms of Service found for domain '{clean_domain}'",
                "domain_folder": str(domain_folder)
            }
        
        # Collect all files from all doc types
        all_content = []
        total_files = 0
        
        for doc_type_name in doc_types:
            target_folder = domain_folder / doc_type_name
            md_files = self.get_markdown_files_sorted(target_folder)
            
            for md_file in md_files:
                content = self.read_markdown_file(md_file)
                # Add separator with metadata
                separator = f"\n\n{'='*80}\n"
                separator += f"Document Type: {doc_type_name}\n"
                separator += f"Version Date: {md_file.stem}\n"
                separator += f"File: {md_file.name}\n"
                separator += f"{'='*80}\n\n"
                
                all_content.append(separator + content)
                total_files += 1
        
        # Chain all content together
        chained_content = "\n\n".join(all_content)
        
        return {
            "EULA": chained_content,
            "metadata": {
                "domain": clean_domain,
                "document_types": doc_types,
                "total_versions": total_files,
                "versions_per_type": {
                    dt: len(self.get_markdown_files_sorted(domain_folder / dt))
                    for dt in doc_types
                }
            }
        }
