"""
Database module for the Voting App.

This module handles all database operations including:
- Connection management
- Data models
- Schema definition
"""

from .connection import get_db_connection
from .models import register_voter, check_voter_voted, record_vote, get_candidates, get_candidate, get_vote_statistics

__all__ = [
    'get_db_connection',
    'register_voter',
    'check_voter_voted',
    'record_vote',
    'get_candidates',
    'get_candidate',
    'get_vote_statistics'
] 