"""
Legal-SKY Python Modules
Converted from Databricks notebooks to production-ready Python modules
"""

__version__ = "1.0.0"
__author__ = "Legal-SKY Team"

# Main entry point
from .legal_wrapper import handle_user_query

__all__ = ["handle_user_query"]
